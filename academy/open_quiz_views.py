"""Umumiy test havolasi: bitta havola — ko'p qatnashchi (F.I.Sh. bilan).

Ustoz havolani yaratadi va (ixtiyoriy) bir nechta email manzilga birdaniga yuboradi.
Qatnashchi havolani ochib, F.I.Sh.ini kiritadi va testni boshlaydi; natijalar ustozning
havola sahifasida F.I.Sh. bo'yicha ko'rinadi. Test yechish mexanizmi (vaqt, saqlash,
oynadan chiqishlar, baholash) shaxsiy havola bilan bir xil — ``views`` dagi yordamchilar.
"""

import re
import secrets
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Avg, Count, F, Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST

from . import mailer
from .forms import OpenQuizForm, OpenQuizInviteForm
from .models import OpenAttempt, OpenQuiz, OpenQuizInvite, QuizLanguage, name_key
from .quiz_i18n import open_message_parts, open_quiz_texts
from .views import (
    _is_owner,
    _owner_cookie,
    _quiz_page,
    _shuffled_questions,
    csv_response,
    review_in_shown_order,
    save_answers,
    submit_answers,
    switch_language,
)

# F.I.Sh.: kamida ikki so'z (familiya va ism), harflar, apostrof va chiziqcha.
NAME_WORD = re.compile(r"^[^\W\d_](?:[^\W\d_]|['ʻʼ‘’`-])*$")


# --- Ustoz -----------------------------------------------------------------------


def _finish_expired(open_quiz: OpenQuiz) -> None:
    """Vaqti tugagan, lekin yakunlanmagan urinishlar (brauzer yopilgan) — oxirgi saqlangan
    javoblar bilan baholanadi, ustoz to'liq natijani ko'radi."""
    cutoff = timezone.now() - timedelta(seconds=OpenAttempt.GRACE_SECONDS)
    for attempt in open_quiz.attempts.filter(status=OpenAttempt.Status.ACTIVE, deadline__lt=cutoff):
        attempt.finish(timed_out=True)


def _public_link(request, open_quiz: OpenQuiz) -> str:
    return request.build_absolute_uri(open_quiz.get_public_url())


def send_invites(request, open_quiz: OpenQuiz, emails: list[str]) -> None:
    """Havolani har bir manzilga alohida xat bilan yuboradi (bitta SMTP ulanishi) va
    natijani ``OpenQuizInvite`` ga yozadi."""
    if not emails:
        return
    link = _public_link(request, open_quiz)
    m = open_message_parts(open_quiz, open_quiz.language)
    text = f"{m['msg_open_hello']}\n{m['msg_quiz']}\n{m['msg_open_how']}\n\n{link}\n\n{m['msg_open_once']}"
    html = mailer.button_html(
        m["msg_title"],
        [m["msg_open_hello"], m["msg_quiz"], m["msg_open_how"]],
        url=link,
        button=m["msg_button"],
        footer=m["msg_open_once"],
        fallback=m["msg_fallback"],
    )
    mails = [mailer.Mail(key=email, to=email, subject=m["msg_subject"], text=text, html=html) for email in emails]
    try:
        results = mailer.send_mails(mails)
    except mailer.MailError as exc:
        messages.error(request, str(exc))
        return
    now = timezone.now()
    OpenQuizInvite.objects.bulk_create(
        OpenQuizInvite(open_quiz=open_quiz, email=r.key, sent_at=now if r.ok else None, error=r.error or "")
        for r in results
    )
    sent = sum(r.ok for r in results)
    if sent:
        messages.success(request, _("Havola {sent} ta manzilga yuborildi.").format(sent=sent))
    failed = [f"{r.key} ({r.error})" for r in results if not r.ok]
    if failed:
        messages.error(
            request, _("Yuborilmadi: {failed}").format(failed="; ".join(failed[:5]) + ("…" if len(failed) > 5 else ""))
        )


@login_required
def open_quiz_list(request):
    open_quizzes = (
        OpenQuiz.objects.select_related("quiz__topic")
        .annotate(
            joined_n=Count("attempts", distinct=True),
            done_n=Count("attempts", filter=Q(attempts__status=OpenAttempt.Status.FINISHED), distinct=True),
            invited_n=Count("invites", filter=Q(invites__sent_at__isnull=False), distinct=True),
        )
        .order_by("-created_at", "-pk")
    )
    return render(request, "academy/quiz/open_list.html", {"open_quizzes": open_quizzes, "now": timezone.now()})


@login_required
def open_quiz_create(request):
    form = OpenQuizForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        open_quiz = form.save()
        messages.success(request, _("Umumiy havola yaratildi."))
        send_invites(request, open_quiz, form.cleaned_data["emails"])
        return redirect(open_quiz)
    return render(request, "academy/quiz/open_form.html", {"form": form})


SORTS = {
    "yangi": ("-started_at", "-pk"),
    "ball": (F("correct").desc(nulls_last=True), "started_at"),
    "ism": ("name_key",),
}


@login_required
def open_quiz_detail(request, pk):
    open_quiz = get_object_or_404(OpenQuiz.objects.select_related("quiz__topic"), pk=pk)
    _finish_expired(open_quiz)
    attempts = open_quiz.attempts.all()
    q = request.GET.get("q", "").strip()
    if q:
        attempts = attempts.filter(name_key__contains=name_key(q))
    sort = request.GET.get("sort") if request.GET.get("sort") in SORTS else "yangi"
    attempts = list(attempts.order_by(*SORTS[sort]))
    finished = open_quiz.attempts.filter(status=OpenAttempt.Status.FINISHED)
    stats = finished.aggregate(n=Count("pk"), correct=Avg("correct"), total=Avg("total"))
    avg = round(100 * stats["correct"] / stats["total"]) if stats["total"] else None
    joined_n = open_quiz.attempts.count()
    invites = list(open_quiz.invites.all()[:300])
    return render(
        request,
        "academy/quiz/open_detail.html",
        {
            "oq": open_quiz,
            "link": _public_link(request, open_quiz),
            "attempts": attempts,
            "q": q,
            "sort": sort,
            "joined_n": joined_n,
            "done_n": stats["n"],
            "active_n": joined_n - stats["n"],
            "avg": avg,
            "invites": invites,
            "invite_sent_n": sum(1 for i in invites if i.sent_at),
            "invite_form": OpenQuizInviteForm(),
            "is_open": open_quiz.is_open(),
        },
    )


@login_required
@require_POST
def open_quiz_invite(request, pk):
    open_quiz = get_object_or_404(OpenQuiz, pk=pk)
    form = OpenQuizInviteForm(request.POST)
    if form.is_valid():
        send_invites(request, open_quiz, form.cleaned_data["emails"])
    else:
        messages.error(request, " ".join(form.errors["emails"]))
    return redirect(f"{open_quiz.get_absolute_url()}#invite")


@login_required
@require_POST
def open_quiz_toggle(request, pk):
    open_quiz = get_object_or_404(OpenQuiz, pk=pk)
    open_quiz.is_active = not open_quiz.is_active
    open_quiz.save(update_fields=["is_active"])
    if open_quiz.is_active:
        messages.success(request, _("Havola ochildi."))
    else:
        messages.success(request, _("Havola yopildi — yangi qatnashchi kira olmaydi."))
    return redirect(open_quiz)


@login_required
@require_POST
def open_quiz_delete(request, pk):
    open_quiz = get_object_or_404(OpenQuiz, pk=pk)
    open_quiz.delete()
    messages.success(request, _("Umumiy havola va uning natijalari o‘chirildi."))
    return redirect("open_quiz_list")


@login_required
def open_quiz_export(request, pk):
    open_quiz = get_object_or_404(OpenQuiz.objects.select_related("quiz__topic"), pk=pk)
    _finish_expired(open_quiz)
    labels = dict(OpenAttempt.Status.choices)

    def row(a: OpenAttempt):
        return [
            a.full_name,
            labels.get(a.status, a.status),
            a.correct if a.correct is not None else "",
            a.total or "",
            a.percent if a.percent is not None else "",
            a.duration_text,
            a.leave_count,
            a.get_language_display(),
            timezone.localtime(a.started_at).strftime("%d.%m.%Y %H:%M"),
        ]

    header = ["F.I.Sh.", "Holat", "To‘g‘ri", "Savollar", "Foiz", "Vaqt (daq:s)", "Oynadan chiqish", "Til", "Boshlagan"]
    stamp = timezone.localdate().isoformat()
    rows = (row(a) for a in open_quiz.attempts.order_by("name_key"))
    return csv_response(f"umumiy-test-{open_quiz.pk}-{stamp}.csv", header, rows)


@login_required
def open_attempt_review(request, pk, attempt_pk):
    """Faqat ustoz: qatnashchining har bir savolga javobi va to'g'ri javob."""
    attempt = get_object_or_404(
        OpenAttempt.objects.select_related("open_quiz", "quiz__topic"),
        pk=attempt_pk,
        open_quiz_id=pk,
        status=OpenAttempt.Status.FINISHED,
    )
    items = review_in_shown_order(attempt)
    finished = attempt.open_quiz.attempts.filter(status=OpenAttempt.Status.FINISHED)
    others = list(finished.order_by("name_key").only("pk", "full_name"))
    index = next(i for i, a in enumerate(others) if a.pk == attempt.pk)
    duration = attempt.duration_seconds
    return render(
        request,
        "academy/quiz/open_review.html",
        {
            "oq": attempt.open_quiz,
            "attempt": attempt,
            "topic": attempt.quiz.topic,
            "items": items,
            "wrong_n": sum(not i["is_correct"] for i in items),
            "unanswered_n": sum(not i["answered"] for i in items),
            "only_wrong": request.GET.get("xato") == "1",
            "duration": divmod(duration, 60) if duration is not None else None,
            "prev": others[index - 1] if index > 0 else None,
            "next": others[index + 1] if index + 1 < len(others) else None,
        },
    )


@login_required
@require_POST
def open_attempt_delete(request, pk, attempt_pk):
    """Natijani o'chirish — shu F.I.Sh. bilan testni qayta topshirish imkoni ochiladi."""
    attempt = get_object_or_404(OpenAttempt, pk=attempt_pk, open_quiz_id=pk)
    attempt.delete()
    messages.success(
        request, _("{name} natijasi o‘chirildi — u testni qayta topshirishi mumkin.").format(name=attempt.full_name)
    )
    return redirect("open_quiz", pk=pk)


# --- Qatnashchi (login talab qilinmaydi) -------------------------------------------


def _resume_cookie(open_quiz: OpenQuiz) -> str:
    return f"oq_{open_quiz.pk}"


def _language(request, open_quiz: OpenQuiz) -> str:
    value = request.POST.get("til") or request.GET.get("til")
    return value if value in QuizLanguage.values else open_quiz.language


def _public_page(request, template, context, status=200):
    response = render(request, f"academy/quiz/{template}.html", context, status=status)
    response["X-Robots-Tag"] = "noindex, nofollow"
    return response


def valid_full_name(value: str) -> bool:
    words = value.split()
    return 2 <= len(words) <= 6 and len(value) <= 160 and all(NAME_WORD.match(w) for w in words)


@never_cache
def open_quiz_public(request, token):
    """Kirish sahifasi: F.I.Sh. → "Testni boshlash". GET hech narsani o'zgartirmaydi
    (Telegram/pochta havolani oldindan ochib ko'rishi testni boshlab yubormasin)."""
    open_quiz = get_object_or_404(OpenQuiz.objects.select_related("quiz__topic"), token=token)
    # Shu brauzerda boshlangan urinish bo'lsa — o'shanga (davom ettirish yoki natija).
    resume = request.COOKIES.get(_resume_cookie(open_quiz), "")
    if resume:
        attempt = OpenAttempt.objects.filter(open_quiz=open_quiz, token=resume).first()
        if attempt and _is_owner(request, attempt):
            return redirect(attempt.get_absolute_url())

    lang = _language(request, open_quiz)
    t = open_quiz_texts(open_quiz, lang)
    if not open_quiz.is_open():
        return _public_page(request, "open_closed", {"t": t, "oq": open_quiz}, status=410)
    if not open_quiz.question_total:
        return _public_page(request, "open_closed", {"t": t, "oq": open_quiz, "empty": True}, status=410)

    full_name = " ".join(request.POST.get("full_name", "").split())
    error = ""
    if request.method == "POST":
        if not valid_full_name(full_name):
            error = t["open_name_error"]
        elif OpenAttempt.objects.filter(open_quiz=open_quiz, name_key=name_key(full_name)).exists():
            error = t["open_duplicate"]
        else:
            owner_key = secrets.token_urlsafe(24)
            try:
                attempt = OpenAttempt.begin(open_quiz, full_name, lang, owner_key)
            except IntegrityError:  # bir vaqtda ikki brauzerdan bir xil F.I.Sh.
                error = t["open_duplicate"]
            else:
                response = redirect(attempt.get_absolute_url())
                max_age = open_quiz.time_limit_minutes * 60 + 30 * 24 * 3600
                cookie = {"max_age": max_age, "secure": request.is_secure(), "httponly": True, "samesite": "Lax"}
                response.set_cookie(_owner_cookie(attempt), owner_key, path=attempt.get_absolute_url(), **cookie)
                response.set_cookie(
                    _resume_cookie(open_quiz), attempt.token, path=open_quiz.get_public_url(), **cookie
                )
                return response
    return _public_page(
        request,
        "open_start",
        {"t": t, "oq": open_quiz, "lang": lang, "full_name": full_name, "error": error},
        status=400 if error else 200,
    )


def _open_attempt(token, attempt_token) -> OpenAttempt:
    attempt = (
        OpenAttempt.objects.select_related("open_quiz", "quiz__topic")
        .filter(open_quiz__token=token, token=attempt_token)
        .first()
    )
    if attempt is None:
        raise Http404
    return attempt


@never_cache
def open_quiz_take(request, token, attempt_token):
    attempt = _open_attempt(token, attempt_token)
    owner = _is_owner(request, attempt)
    if attempt.status == OpenAttempt.Status.ACTIVE and attempt.is_expired(grace=OpenAttempt.GRACE_SECONDS):
        attempt.finish(timed_out=True)
    if not owner:
        return _quiz_page(request, attempt, "used", status=410)
    if attempt.status == OpenAttempt.Status.FINISHED:
        return _quiz_page(request, attempt, "result", items=[])
    return _quiz_page(
        request, attempt, "take", questions=_shuffled_questions(attempt), seconds_left=attempt.seconds_left()
    )


@never_cache
@require_POST
def open_quiz_save(request, token, attempt_token):
    return save_answers(request, _open_attempt(token, attempt_token))


@never_cache
@require_POST
def open_quiz_language(request, token, attempt_token):
    attempt = _open_attempt(token, attempt_token)
    switch_language(request, attempt)
    return redirect(attempt.get_absolute_url())


@never_cache
@require_POST
def open_quiz_submit(request, token, attempt_token):
    attempt = _open_attempt(token, attempt_token)
    submit_answers(request, attempt)
    return redirect(attempt.get_absolute_url())
