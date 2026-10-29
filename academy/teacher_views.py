"""O'qituvchilar: o'qituvchining sahifasi, Telegramni QR orqali ulash va bosh ustozning boshqaruvi."""

from datetime import date
from functools import wraps

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST

from . import audit, qr, teachers
from . import teacher_report as report
from .forms import TeacherForm
from .models import ActionLog, Group, QuizBatch, TeacherAccount, TeacherPayout
from .templatetags.ui import intspace
from .views import csv_response

User = get_user_model()


def superuser_required(view):
    @wraps(view)
    @login_required
    def wrapper(request, *args, **kwargs):
        if not request.user.is_superuser:
            raise Http404
        return view(request, *args, **kwargs)

    return wrapper


def teacher_required(view):
    @wraps(view)
    @login_required
    def wrapper(request, *args, **kwargs):
        if not teachers.is_teacher(request.user):
            return redirect("dashboard")
        return view(request, *args, **kwargs)

    return wrapper


# --- O'qituvchi ---------------------------------------------------------------------


@teacher_required
def teacher_home(request):
    """O'qituvchining sahifasi: o'z guruhlari, test jo'natish va so'nggi natijalar."""
    groups = list(
        teachers.teacher_groups(request.user)
        .filter(status=Group.Status.ACTIVE)
        .order_by("name")
        .prefetch_related("students")
    )
    batches = (
        QuizBatch.objects.filter(group__in=groups, from_profile=False)
        .select_related("quiz__topic", "group")
        .order_by("-created_at")[:15]
    )
    account = teachers.account_of(request.user)
    return render(
        request,
        "academy/teachers/home.html",
        {
            "groups": groups,
            "batches": batches,
            "account": account,
            "month_row": report.teacher_row(account, report.month_start()),  # bu oy: darslar va maosh
        },
    )


def _link_state(account: TeacherAccount) -> dict:
    return {
        "status": account.link_status or "",
        "qr": str(qr.svg(account.link_url)) if account.link_status == account.Link.QR and account.link_url else "",
        "error": account.link_error,
        "linked": account.is_linked,
        "next": reverse("teacher_home"),
    }


@never_cache
@teacher_required
def teacher_telegram(request):
    """Birinchi kirish: Telegramni QR orqali ulash (ulangan bo'lsa — qayta so'ralmaydi)."""
    account = teachers.account_of(request.user)
    if account.is_linked:
        return redirect("teacher_home")
    if account.link_status != account.Link.ERROR:
        teachers.start_link(account)
        account.refresh_from_db()
    return render(request, "academy/teachers/telegram.html", {"account": account, "state": _link_state(account)})


@never_cache
@teacher_required
def teacher_telegram_status(request):
    account = teachers.account_of(request.user)
    stopped = account.link_status != account.Link.ERROR and not teachers.link_running(account)
    if not account.is_linked and stopped:
        teachers.start_link(account)  # jarayon to'xtagan (masalan, server qayta ishga tushgan) — qaytadan
        account.refresh_from_db()
    return JsonResponse(_link_state(account))


@never_cache
@require_POST
@teacher_required
def teacher_telegram_password(request):
    account = teachers.account_of(request.user)
    password = request.POST.get("password", "")
    if account.link_status == account.Link.PASSWORD and password:
        TeacherAccount.objects.filter(pk=account.pk).update(link_password=password[:255], link_error="")
    return JsonResponse({"ok": True})


@require_POST
@teacher_required
def teacher_telegram_restart(request):
    account = teachers.account_of(request.user)
    if not account.is_linked:
        TeacherAccount.objects.filter(pk=account.pk).update(link_status=TeacherAccount.Link.NONE, link_error="")
        account.refresh_from_db()
        teachers.start_link(account)
    return redirect("teacher_telegram")


# --- Bosh ustoz: o'qituvchilarni boshqarish -----------------------------------------------


def _save_teacher(form: TeacherForm, user=None):
    data = form.cleaned_data
    with transaction.atomic():
        if user is None:
            user = User(username=data["username"])
        user.username = data["username"]
        user.first_name = data["first_name"]
        user.last_name = data["last_name"]
        user.is_active = data.get("is_active", True)
        user.is_staff = user.is_superuser = False
        if data.get("password"):
            user.set_password(data["password"])
        user.save()
        account = teachers.account_of(user)
        account.lesson_rate = data.get("lesson_rate") or 0
        account.monthly_fixed = data.get("monthly_fixed") or 0
        account.permissions = [key for key in teachers.SECTION_KEYS if key in set(data.get("permissions") or [])]
        account.save(update_fields=["permissions", "lesson_rate", "monthly_fixed"])
        chosen = {g.pk for g in data["groups"]}
        Group.objects.filter(teacher=user).exclude(pk__in=chosen).update(teacher=None)
        Group.objects.filter(pk__in=chosen).update(teacher=user)
    return user


@superuser_required
def teacher_list(request):
    form = TeacherForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = _save_teacher(form)
        messages.success(
            request,
            _("O‘qituvchi yaratildi: login “{username}”. Birinchi kirishda Telegramini QR-kod orqali ulaydi.").format(
                username=user.username
            ),
        )
        return redirect("teacher_list")
    rows = (
        TeacherAccount.objects.select_related("user")
        .filter(user__is_superuser=False)
        .order_by("user__first_name", "user__username")
    )
    groups_by_teacher: dict[int, list] = {}
    for g in Group.objects.filter(teacher__isnull=False).order_by("name"):
        groups_by_teacher.setdefault(g.teacher_id, []).append(g)
    labels = {key: label for key, label, _pages in teachers.SECTIONS}
    teachers_list = [
        {
            "account": a,
            "groups": groups_by_teacher.get(a.user_id, []),
            "sections": [labels[k] for k in teachers.SECTION_KEYS if k in set(a.permissions or [])],
        }
        for a in rows
    ]
    return render(request, "academy/teachers/list.html", {"form": form, "teachers": teachers_list})


@superuser_required
def teacher_edit(request, pk):
    user = get_object_or_404(User, pk=pk, is_superuser=False)
    account = teachers.account_of(user)
    form = TeacherForm(request.POST or None, user=user)
    if request.method == "POST" and form.is_valid():
        _save_teacher(form, user)
        messages.success(request, _("O‘qituvchi saqlandi."))
        return redirect("teacher_list")
    return render(request, "academy/teachers/edit.html", {"form": form, "teacher": user, "account": account})


@superuser_required
def teacher_report(request):
    """Bosh ustoz: o'qituvchilar faoliyati va maoshi oy bo'yicha (?oy=YYYY-MM, ?csv=1)."""
    month = report.month_start(request.GET.get("oy", ""))
    rows = report.month_report(month)
    if request.GET.get("csv") == "1":
        header = [
            "O‘qituvchi", "Login", "Guruhlar", "O‘quvchilar", "O‘tilgan darslar", "Bekor", "Rejada",
            "Yuborilgan testlar", "Yakunlangan testlar", "O‘rtacha natija %", "Davomat %",
            "Dars narxi", "Oylik qat’iy", "Hisoblangan", "To‘langan",
        ]  # fmt: skip
        data = [
            [
                r.user.get_full_name() or r.user.username,
                r.user.username,
                ", ".join(g.code for g in r.groups),
                r.students,
                r.lessons,
                r.cancelled,
                r.planned,
                r.tests,
                r.results,
                "" if r.avg_percent is None else r.avg_percent,
                "" if r.attendance is None else r.attendance,
                r.account.lesson_rate,
                r.account.monthly_fixed,
                r.salary,
                r.payout.amount if r.payout else "",
            ]
            for r in rows
        ]
        return csv_response(f"oqituvchilar-{month:%Y-%m}.csv", header, data)
    return render(
        request,
        "academy/teachers/report.html",
        {
            "rows": rows,
            "month": month,
            "prev": report.prev_month(month),
            "next": report.next_month(month),
            "is_current": month == report.month_start(),
            "total_salary": sum(r.salary for r in rows),
            "total_paid": sum(r.payout.amount for r in rows if r.payout),
            "total_lessons": sum(r.lessons for r in rows),
        },
    )


@require_POST
@superuser_required
def teacher_payout(request, pk):
    """Shu oy maoshi to'landi deb belgilash (yoki bekor qilish)."""
    user = get_object_or_404(User, pk=pk, is_superuser=False)
    month = report.month_start(request.POST.get("oy", ""))
    back = f"{reverse('teacher_report')}?oy={month:%Y-%m}"
    if request.POST.get("action") == "undo":
        TeacherPayout.objects.filter(teacher=user, month=month).delete()
        messages.info(request, _("{name}: to‘lov belgisi olib tashlandi.").format(name=user.get_full_name() or user))
        return redirect(back)
    payout = report.mark_paid(teacher_account_or_404(user), month)
    messages.success(
        request,
        _("{name}: {month} uchun {amount} so‘m to‘landi deb belgilandi.").format(
            name=user.get_full_name() or user.username, month=f"{month:%m.%Y}", amount=intspace(payout.amount)
        ),
    )
    return redirect(back)


def teacher_account_or_404(user) -> TeacherAccount:
    account = TeacherAccount.objects.filter(user=user).first()
    if account is None:
        raise Http404
    return account


@superuser_required
def action_log(request):
    """Bosh ustoz: harakatlar jurnali (?user=, ?kun=YYYY-MM-DD, ?amal=)."""
    logs = ActionLog.objects.select_related("user")
    user_id = request.GET.get("user", "")
    if user_id.isdigit():
        logs = logs.filter(user_id=user_id)
    day = request.GET.get("kun", "")
    try:
        logs = logs.filter(created_at__date=date.fromisoformat(day)) if day else logs
    except ValueError:
        day = ""
    action = request.GET.get("amal", "")
    if action:
        logs = logs.filter(action=action)
    page = Paginator(logs, 100).get_page(request.GET.get("page"))
    users = User.objects.filter(actions__isnull=False).distinct().order_by("first_name", "username")
    actions = sorted(
        {(a, audit.label(a)) for a in ActionLog.objects.values_list("action", flat=True).distinct()},
        key=lambda pair: pair[1],
    )
    return render(
        request,
        "academy/teachers/action_log.html",
        {
            "page": page,
            "users": users,
            "actions": actions,
            "user_id": int(user_id) if user_id.isdigit() else None,
            "day": day,
            "action": action,
        },
    )


@require_POST
@superuser_required
def teacher_unlink(request, pk):
    user = get_object_or_404(User, pk=pk, is_superuser=False)
    teachers.unlink(teachers.account_of(user))
    messages.info(
        request,
        _("{name}: Telegram uzildi — keyingi kirishda QR-kod orqali qayta ulaydi.").format(
            name=user.get_full_name() or user.username
        ),
    )
    return redirect("teacher_edit", pk=user.pk)
