"""O'quvchi profili (login'siz, maxfiy havola) va ustozning profil boshqaruvi.

Mantiq ``academy.profiles`` da; bu yerda faqat so'rov/javob.
"""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST

from . import coins, profiles
from .models import QuizAttempt, Student, TestRequest, Topic


def _student(token) -> Student:
    if not token:  # o'chirilgan havola (bo'sh kalit) hech qachon mos kelmasin
        raise Http404
    return get_object_or_404(Student.objects.select_related("group"), portal_token=token)


def _portal_url(token, anchor="") -> str:
    return reverse("student_portal", args=[token]) + (f"#{anchor}" if anchor else "")


def _page(request, template, context, status=200):
    response = render(request, f"academy/portal/{template}.html", context, status=status)
    response["X-Robots-Tag"] = "noindex, nofollow"
    return response


# --- O'quvchi --------------------------------------------------------------------


@never_cache
@require_POST
def portal_access_request(request, token):
    profiles.request_access(_student(token))
    return redirect(_portal_url(token))


@never_cache
@require_POST
def portal_test_request(request, token, topic_id):
    """O'quvchi testni o'zi boshlaydi (ustoz ruxsati shart emas) → savollar soni va vaqt."""
    student = _student(token)
    topic = get_object_or_404(Topic, pk=topic_id)
    try:
        req = profiles.begin_test(student, topic)
    except profiles.ProfileError as exc:
        messages.error(request, str(exc))
        return redirect(_portal_url(token, f"t{topic.pk}"))
    return redirect("portal_test_start", token=token, pk=req.pk)


@never_cache
def portal_test_start(request, token, pk):
    """Ruxsat berilgan so'rov: o'quvchi savollar soni va vaqtni tanlaydi → boshlash sahifasi."""
    student = _student(token)
    if not profiles.is_open(student):
        return redirect(_portal_url(token))
    req = get_object_or_404(TestRequest.objects.select_related("topic"), pk=pk, student=student)
    if req.status == TestRequest.Status.USED and req.attempt:
        return redirect(req.attempt.get_absolute_url())
    if req.status != TestRequest.Status.APPROVED:
        return redirect(_portal_url(token, f"t{req.topic_id}"))
    error = ""
    if request.method == "POST":
        try:
            questions = int(request.POST.get("questions", 0))
            minutes = int(request.POST.get("minutes", 0))
            attempt = profiles.start_test(req, questions, minutes)
        except (ValueError, profiles.ProfileError) as exc:
            error = str(exc) if isinstance(exc, profiles.ProfileError) else "Tanlovni tekshiring."
        else:
            return redirect(attempt.get_absolute_url())
    return _page(
        request,
        "start",
        {
            "student": student,
            "req": req,
            "bank": req.topic.quiz.questions.count(),
            "question_choices": TestRequest.QUESTION_CHOICES,
            "minute_choices": TestRequest.MINUTE_CHOICES,
            "error": error,
        },
        status=422 if error else 200,
    )


@never_cache
def portal_study(request, token, topic_id):
    """"Darsni qayta mustahkamlash": mavzu materiali, bajarilgan misollar, qayta topshirish."""
    student = _student(token)
    if not profiles.is_open(student):
        return redirect(_portal_url(token))
    topic = get_object_or_404(Topic.objects.select_related("module"), pk=topic_id)
    row = profiles.open_study(student, topic)
    if row is None:
        raise Http404
    return _page(
        request,
        "study",
        {
            "student": student,
            "topic": topic,
            "row": row,
            "material": topic.study_in(student.quiz_language),
            "pass_percent": profiles.PASS_PERCENT,
        },
    )


# --- Ustoz -----------------------------------------------------------------------


def _back(request, student) -> str:
    return request.POST.get("next") == "requests" and reverse("quiz_review_requests") or (
        f"{student.get_absolute_url()}#profile"
    )


@login_required
@require_POST
def student_profile_access(request, pk):
    student = get_object_or_404(Student, pk=pk)
    action = request.POST.get("action", "")
    if action.isdigit() and int(action) in profiles.ACCESS_HOURS:
        profiles.grant_access(student, int(action))
        messages.success(
            request, f"{student.full_name}: profil {action} soatga ochildi."
        )
    else:
        profiles.close_access(student)
        messages.info(request, f"{student.full_name}: profilga kirish yopildi.")
    return redirect(_back(request, student))


@login_required
@require_POST
def student_allowed_topics(request, pk):
    student = get_object_or_404(Student.objects.select_related("group"), pk=pk)
    if request.POST.get("action") == "taught":
        ids = profiles.taught_topic_ids(student)
        student.allowed_topics.add(*ids)
        messages.success(request, f"O‘tilgan {len(ids)} ta mavzu qo‘shildi.")
    else:
        ids = [int(v) for v in request.POST.getlist("topics") if v.isdigit()]
        student.allowed_topics.set(Topic.objects.filter(pk__in=ids))
        messages.success(request, f"Test uchun ruxsat etilgan mavzular: {len(ids)} ta.")
    return redirect(f"{student.get_absolute_url()}#profile")


@login_required
@require_POST
def test_request_decide(request, pk):
    req = get_object_or_404(TestRequest.objects.select_related("student", "topic"), pk=pk)
    approve = request.POST.get("action") == "approve"
    profiles.decide_test(req, approve)
    messages.success(
        request,
        f"{req.student.full_name} — “{req.topic.title}”: "
        + ("ruxsat berildi." if approve else "rad etildi."),
    )
    return redirect(_back(request, req.student))


def profile_context(student) -> dict:
    """Ustozning o'quvchi kartasi uchun: profil holati, mavzular, so'rovlar."""
    taught = profiles.taught_topic_ids(student)
    allowed = set(student.allowed_topics.values_list("pk", flat=True))
    topics = Topic.objects.filter(quiz__questions__isnull=False).distinct().select_related("module")
    return {
        "profile_open": profiles.is_open(student),
        "access_hours": profiles.ACCESS_HOURS,
        "profile_topics": [
            {"topic": t, "allowed": t.pk in allowed, "taught": t.pk in taught} for t in topics
        ],
        "allowed_n": len(allowed),
        "taught_missing": len(taught - allowed),
        "profile_requests": student.test_requests.select_related("topic", "attempt")[:8],
        "coin_balance": coins.balance(student),
        "coin_history": student.coins.select_related("attempt__quiz__topic")[:8],
        "profile_attempts_n": QuizAttempt.objects.filter(student=student, batch__from_profile=True).count(),
    }
