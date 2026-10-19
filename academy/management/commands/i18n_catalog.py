"""Tarjima katalogi: shablon va Python'dagi matnlarni yig'ish, .po yozish, .mo kompilyatsiya.

GNU gettext (xgettext/msgfmt) talab qilinmaydi — hammasi Python'da:

    python manage.py i18n_catalog            # locale/ru/LC_MESSAGES/django.po ni yangilaydi
                                             # (mavjud tarjimalar saqlanadi) va .mo ni yig'adi
    python manage.py i18n_catalog --check    # tarjimasi yo'q matnlar bo'lsa — xato (CI uchun)

Kalitlar (msgid) Django'ning o'z mexanizmi bilan hisoblanadi (BlockTranslateNode.
render_token_list), shuning uchun ishlash vaqtidagi qidiruv bilan aynan mos keladi.
"""

import ast
import struct
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.template import engines
from django.template.base import FilterExpression, Node, Variable
from django.templatetags.i18n import BlockTranslateNode, TranslateNode

PY_DIRS = ["academy", "config"]
PY_SKIP = {"migrations", "tests", "school_data"}
GETTEXT_NAMES = {"_", "gettext", "gettext_lazy", "gettext_noop", "pgettext", "pgettext_lazy"}


def template_msgids() -> dict[str, set[str]]:
    engine = engines["django"].engine
    found: dict[str, set[str]] = {}
    roots = [Path(d) for d in engine.dirs] + [Path(settings.BASE_DIR) / "academy" / "templates"]
    for root in roots:
        for path in sorted(root.rglob("*.html")):
            name = str(path.relative_to(root))
            tpl = engine.get_template(name)
            ref = f"{root.name}/{name}"

            def add(msgid, ref=ref):
                if msgid:
                    found.setdefault(msgid, set()).add(ref)

            for node in tpl.nodelist.get_nodes_by_type(TranslateNode):
                var = node.filter_expression.var
                if isinstance(var, Variable) and var.literal is not None:
                    add(str(var.literal))
            for node in tpl.nodelist.get_nodes_by_type(BlockTranslateNode):
                add(node.render_token_list(node.singular)[0])
            for node in tpl.nodelist.get_nodes_by_type(Node):
                for value in _filter_expressions(node):
                    var = value.var
                    if isinstance(var, Variable) and var.translate and var.literal is not None:
                        add(str(var.literal))
                    for _func, args in value.filters:
                        for _lookup, arg in args:
                            if isinstance(arg, Variable) and arg.translate and arg.literal is not None:
                                add(str(arg.literal))
    return found


def _filter_expressions(node):
    for value in vars(node).values():
        if isinstance(value, FilterExpression):
            yield value
        elif isinstance(value, dict):
            yield from (v for v in value.values() if isinstance(v, FilterExpression))
        elif isinstance(value, (list, tuple)):
            yield from (v for v in value if isinstance(v, FilterExpression))


def python_msgids() -> dict[str, set[str]]:
    found: dict[str, set[str]] = {}
    base = Path(settings.BASE_DIR)
    for d in PY_DIRS:
        for path in sorted((base / d).rglob("*.py")):
            if PY_SKIP & set(path.relative_to(base).parts):
                continue
            tree = ast.parse(path.read_text())
            for n in ast.walk(tree):
                if (
                    isinstance(n, ast.Call)
                    and isinstance(n.func, ast.Name)
                    and n.func.id in GETTEXT_NAMES
                    and n.args
                    and isinstance(n.args[0], ast.Constant)
                    and isinstance(n.args[0].value, str)
                ):
                    found.setdefault(n.args[0].value, set()).add(f"{path.relative_to(base)}:{n.lineno}")
    return found


# --- .po o'qish/yozish ---------------------------------------------------------


def _po_escape(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\t", "\\t")


def _po_unescape(s: str) -> str:
    out, i = [], 0
    while i < len(s):
        c = s[i]
        if c == "\\" and i + 1 < len(s):
            nxt = s[i + 1]
            out.append({"n": "\n", "t": "\t", '"': '"', "\\": "\\"}.get(nxt, nxt))
            i += 2
        else:
            out.append(c)
            i += 1
    return "".join(out)


def read_po(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    entries, cur, field = {}, {"msgid": "", "msgstr": ""}, None

    def flush():
        if cur["msgid"]:
            entries[cur["msgid"]] = cur["msgstr"]

    for line in path.read_text().splitlines():
        line = line.strip()
        if line.startswith("msgid "):
            flush()
            cur = {"msgid": "", "msgstr": ""}
            field = "msgid"
            cur[field] = _po_unescape(line[6:].strip()[1:-1])
        elif line.startswith("msgstr "):
            field = "msgstr"
            cur[field] = _po_unescape(line[7:].strip()[1:-1])
        elif line.startswith('"') and field:
            cur[field] += _po_unescape(line[1:-1])
    flush()
    return entries


def write_po(path: Path, refs: dict[str, set[str]], translations: dict[str, str]) -> None:
    lines = [
        "# Minar Test — ruscha tarjima.",
        "# Yangilash: python manage.py i18n_catalog",
        'msgid ""',
        'msgstr ""',
        '"Content-Type: text/plain; charset=UTF-8\\n"',
        '"Language: ru\\n"',
        '"Plural-Forms: nplurals=3; plural=(n%10==1 && n%100!=11 ? 0 : n%10>=2 && n%10<=4 && "'
        '"(n%100<10 || n%100>=20) ? 1 : 2);\\n"',
        "",
    ]
    for msgid in sorted(refs, key=lambda m: (sorted(refs[m])[0], m)):
        lines.append("#: " + " ".join(sorted(refs[msgid])[:4]))
        lines.append(f'msgid "{_po_escape(msgid)}"')
        lines.append(f'msgstr "{_po_escape(translations.get(msgid, ""))}"')
        lines.append("")
    path.write_text("\n".join(lines))


def write_mo(path: Path, translations: dict[str, str]) -> None:
    """GNU .mo (little-endian) — faqat tarjimasi borlar."""
    header = (
        "Content-Type: text/plain; charset=UTF-8\n"
        "Language: ru\n"
        "Plural-Forms: nplurals=3; plural=(n%10==1 && n%100!=11 ? 0 : n%10>=2 && n%10<=4 && "
        "(n%100<10 || n%100>=20) ? 1 : 2);\n"
    )
    items = sorted([("", header)] + [(k, v) for k, v in translations.items() if v])
    ids = [k.encode() for k, _v in items]
    strs = [v.encode() for _k, v in items]
    n = len(items)
    keystart = 7 * 4 + 16 * n
    valuestart = keystart + sum(len(i) + 1 for i in ids)
    koffsets, voffsets, kpos, vpos = [], [], keystart, valuestart
    for i, s in zip(ids, strs, strict=True):
        koffsets += [len(i), kpos]
        voffsets += [len(s), vpos]
        kpos += len(i) + 1
        vpos += len(s) + 1
    out = struct.pack("Iiiiiii", 0x950412DE, 0, n, 7 * 4, 7 * 4 + n * 8, 0, 0)
    out += struct.pack(f"{2 * n}i", *koffsets) + struct.pack(f"{2 * n}i", *voffsets)
    out += b"".join(i + b"\0" for i in ids) + b"".join(s + b"\0" for s in strs)
    path.write_bytes(out)


class Command(BaseCommand):
    help = "Ruscha tarjima katalogini yangilaydi (.po) va kompilyatsiya qiladi (.mo)."

    def add_arguments(self, parser):
        parser.add_argument("--check", action="store_true", help="Tarjimasi yo'q matn bo'lsa — xato")

    def handle(self, *args, check, **options):
        refs = template_msgids()
        for k, v in python_msgids().items():
            refs.setdefault(k, set()).update(v)
        po = Path(settings.BASE_DIR) / "locale" / "ru" / "LC_MESSAGES" / "django.po"
        po.parent.mkdir(parents=True, exist_ok=True)
        old = read_po(po)
        translations = {k: old.get(k, "") for k in refs}
        missing = sorted(k for k, v in translations.items() if not v)
        if check:
            if missing:
                raise CommandError(f"Tarjimasi yo'q {len(missing)} ta matn, masalan: {missing[:3]}")
            self.stdout.write(f"Hamma {len(refs)} ta matn tarjima qilingan.")
            return
        write_po(po, refs, translations)
        write_mo(po.with_suffix(".mo"), translations)
        unused = len(set(old) - set(refs))
        self.stdout.write(
            f"Matnlar: {len(refs)}, tarjima qilingan: {len(refs) - len(missing)}, "
            f"yo'q: {len(missing)}, eskirgan (olib tashlandi): {unused}."
        )
