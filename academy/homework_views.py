"""Uyga vazifa: o'quvchi profilida topshirish, o'qituvchi/bosh ustoz baholashi va fayllar (faqat ruxsat bilan)."""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST

from . import homework, profiles, teachers
from .models import HomeworkSubmission, Lesson
from .profile_views import _page, _portal_url, _student


def _file_response(sub: HomeworkSubmission):
    if not sub.file:
        raise Http404
    try:
        handle = sub.file.open("rb")
    except FileNotFoundError:
        raise Http404 from None
    response = FileResponse(handle, as_attachment=True, filename=sub.file_name or sub.file.name.rsplit("/", 1)[-1])
    response["X-Content-Type-Options"] = "nosniff"
    response["Cache-Control"] = "private, no-store"
    return response


# --- O'quvchi (profil) ------------------------------------------------------------------


@never_cache
def portal_homework(request, token, lesson_id):
    """Uyga vazifani topshirish (yoki baholanmaguncha yangilash) va natijani ko'rish."""
    student = _student(request, token)
    if not profiles.is_open(student):
        return redirect(_portal_url(token))
    lesson = get_object_or_404(
        Lesson.objects.select_related("topic"), pk=lesson_id, group_id=student.group_id
    )
    if not lesson.homework:
        raise Http404
    sub = HomeworkSubmission.objects.filter(student=student, lesson=lesson).first()
    error = ""
    if request.method == "POST":
        try:
            homework.submit(
                student,
                lesson,
                request.POST.get("text", ""),
                request.POST.get("link", ""),
                request.FILES.get("file"),
            )
        except homework.HomeworkError as exc:
            error = str(exc)
        else:
            messages.success(request, _("Vazifa topshirildi ✅ Ustozingiz tekshirgach, bahosi shu yerda ko‘rinadi."))
            return redirect("portal_homework", token=token, lesson_id=lesson.pk)
    return _page(
        request,
        "homework",
        {
            "student": student,
            "lesson": lesson,
            "sub": sub,
            "due": homework.due_date(lesson),
            "error": error,
            "coins": homework.COINS,
            "pass_score": homework.PASS_SCORE,
            "max_mb": homework.MAX_FILE_BYTES // (1024 * 1024),
            "posted": request.POST if error else None,
        },
        status=422 if error else 200,
    )


@never_cache
def portal_homework_file(request, token, pk):
    student = _student(request, token)
    return _file_response(get_object_or_404(HomeworkSubmission, pk=pk, student=student))


# --- O'qituvchi / bosh ustoz ---------------------------------------------------------------


@login_required
def homework_list(request):
    """Topshirilgan uyga vazifalar: tekshirilmaganlar (standart) yoki hammasi."""
    show_all = request.GET.get("hammasi") == "1"
    subs = teachers.scope(
        request.user, HomeworkSubmission.objects.all(), "student__group__teacher"
    ).select_related("student__group", "lesson__topic", "checked_by")
    pending_n = subs.filter(status=HomeworkSubmission.Status.SUBMITTED).count()
    if not show_all:
        subs = subs.filter(status=HomeworkSubmission.Status.SUBMITTED).order_by("submitted_at")
    page = Paginator(subs, 50).get_page(request.GET.get("page"))
    return render(
        request,
        "academy/homework/list.html",
        {"page": page, "show_all": show_all, "pending_n": pending_n, "coins": homework.COINS},
    )


@login_required
@require_POST
def homework_check(request, pk):
    sub = get_object_or_404(HomeworkSubmission.objects.select_related("student"), pk=pk)
    teachers.check_group(request.user, sub.student.group_id)
    raw = request.POST.get("score", "").strip()
    try:
        given = homework.grade(sub, int(raw) if raw.isdigit() else -1, request.POST.get("comment", ""), request.user)
    except homework.HomeworkError as exc:
        messages.error(request, str(exc))
    else:
        note = _(" +{n} ⚡️ berildi.").format(n=given) if given else ""
        messages.success(request, _("{name}: vazifa baholandi.").format(name=sub.student.full_name) + note)
    back = request.POST.get("next", "")
    return redirect(back if back.startswith("/") and not back.startswith("//") else reverse("homework_list"))


@login_required
def homework_file(request, pk):
    sub = get_object_or_404(HomeworkSubmission.objects.select_related("student"), pk=pk)
    teachers.check_group(request.user, sub.student.group_id)
    return _file_response(sub)
