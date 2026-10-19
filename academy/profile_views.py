"""O'quvchi profili (login'siz, maxfiy havola) va ustozning profil boshqaruvi.

Mantiq ``academy.profiles`` da; bu yerda faqat so'rov/javob.
"""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST

from . import coins, engagement, profiles
from .forms import RewardForm
from .middleware import activate_default_language
from .models import Purchase, QuizAttempt, Reward, Student, TestRequest, Topic


def _student(request, token) -> Student:
    """Profil egasi (maxfiy havola bo'yicha); standart til — uning test tili."""
    if not token:  # o'chirilgan havola (bo'sh kalit) hech qachon mos kelmasin
        raise Http404
    student = get_object_or_404(Student.objects.select_related("group"), portal_token=token)
    activate_default_language(request, student.quiz_language)
    return student


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
    profiles.request_access(_student(request, token))
    return redirect(_portal_url(token))


@never_cache
@require_POST
def portal_test_request(request, token, topic_id):
    """O'quvchi testni o'zi boshlaydi (ustoz ruxsati shart emas) → savollar soni va vaqt."""
    student = _student(request, token)
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
    student = _student(request, token)
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
    student = _student(request, token)
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


@never_cache
def portal_practice(request, token):
    """"Xatolar ustida ishlash": bitta savol — javob — darhol natija (to'g'ri variant ochilmaydi)."""
    student = _student(request, token)
    if not profiles.is_open(student):
        return redirect(_portal_url(token))
    topic_id = request.GET.get("mavzu", "")
    topic_id = int(topic_id) if topic_id.isdigit() else None
    result = None
    if request.method == "POST":
        try:
            result = engagement.answer_mistake(
                student, int(request.POST.get("mistake", 0)), int(request.POST.get("choice", 0) or 0)
            )
        except (ValueError, engagement.EngagementError) as exc:
            messages.error(request, str(exc) if isinstance(exc, engagement.EngagementError) else _("Javobni tanlang."))
        else:
            request.session[f"practice_{student.pk}"] = {
                "correct": result.correct,
                "fixed": result.fixed,
                "left": result.left,
            }
        return redirect(request.get_full_path())
    feedback = request.session.pop(f"practice_{student.pk}", None)
    last = request.GET.get("oldingi", "")
    mistake = engagement.next_mistake(student, topic_id)
    lang = student.quiz_language
    question = choices = None
    if mistake:
        q = mistake.question
        title, _sep, code = q.text_in(lang).partition("\n")
        question = {"title": title, "code": code, "image": q.image.url if q.image else ""}
        choices = [{"pk": c.pk, "text": c.text_in(lang)} for c in engagement.shuffled_choices(mistake, token)]
    return _page(
        request,
        "practice",
        {
            "student": student,
            "mistake": mistake,
            "question": question,
            "choices": choices,
            "feedback": feedback,
            "topics": engagement.mistakes_by_topic(student),
            "topic_id": topic_id,
            "open_n": engagement.open_mistakes(student).count(),
            "fixed_n": student.mistakes.filter(resolved_at__isnull=False).count(),
            "resolve_after": engagement.Mistake.RESOLVE_AFTER,
            "fixed_coins": engagement.MISTAKE_FIXED_COINS,
            "last": last,
        },
    )


@never_cache
@require_POST
def portal_buy(request, token, reward_id):
    student = _student(request, token)
    if not profiles.is_open(student):
        return redirect(_portal_url(token))
    try:
        p = engagement.buy(student, reward_id)
    except engagement.EngagementError as exc:
        messages.error(request, str(exc))
    else:
        messages.success(
            request,
            _("“{title}” so‘rovi ustozga yuborildi. Tasdiqlansa, {cost} coin yechiladi.").format(
                title=p.title, cost=p.cost
            ),
        )
        profiles.notify(f"🛍 {student.full_name} ({student.group.code}): “{p.title}” ({p.cost} coin) so‘radi.")
    return redirect(_portal_url(token, "shop"))


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
            request,
            _("{full_name}: profil {action} soatga ochildi.").format(full_name=student.full_name, action=action),
        )
    else:
        profiles.close_access(student)
        messages.info(request, _("{full_name}: profilga kirish yopildi.").format(full_name=student.full_name))
    return redirect(_back(request, student))


@login_required
@require_POST
def student_allowed_topics(request, pk):
    student = get_object_or_404(Student.objects.select_related("group"), pk=pk)
    if request.POST.get("action") == "taught":
        ids = profiles.taught_topic_ids(student)
        student.allowed_topics.add(*ids)
        messages.success(request, _("O‘tilgan {n} ta mavzu qo‘shildi.").format(n=len(ids)))
    else:
        ids = [int(v) for v in request.POST.getlist("topics") if v.isdigit()]
        student.allowed_topics.set(Topic.objects.filter(pk__in=ids))
        messages.success(request, _("Test uchun ruxsat etilgan mavzular: {n} ta.").format(n=len(ids)))
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
        + (_("ruxsat berildi.") if approve else _("rad etildi.")),
    )
    return redirect(_back(request, req.student))


def profile_context(student) -> dict:
    """Ustozning o'quvchi kartasi uchun: profil holati, mavzular, so'rovlar, coin va streak."""
    taught = profiles.taught_topic_ids(student)
    allowed = set(student.allowed_topics.values_list("pk", flat=True))
    topics = Topic.objects.filter(quiz__questions__isnull=False).distinct().select_related("module")
    return {
        "profile_open": profiles.is_open(student),
        "access_hours": profiles.ACCESS_HOURS,
        "profile_topics": [
            {"topic": t, "allowed": t.pk in allowed, "taught": t.pk in taught} for t in topics
        ],
        "allowed_n": len(allowed | taught),
        "taught_n": len(taught),
        "streak": engagement.streak_info(student),
        "open_mistakes_n": engagement.open_mistakes(student).count(),
        "purchases": student.purchases.all()[:5],
        "profile_requests": student.test_requests.select_related("topic", "attempt")[:8],
        "coin_balance": coins.balance(student),
        "coin_history": student.coins.select_related("attempt__quiz__topic")[:8],
        "profile_attempts_n": QuizAttempt.objects.filter(student=student, batch__from_profile=True).count(),
    }


@login_required
@require_POST
def purchase_decide(request, pk):
    p = get_object_or_404(Purchase.objects.select_related("student"), pk=pk)
    approve = request.POST.get("action") == "approve"
    engagement.decide_purchase(p, approve)
    p.refresh_from_db()
    if approve and p.status != Purchase.Status.APPROVED:
        messages.error(
            request, _("{full_name}: coin yetmaydi — so‘rov rad etildi.").format(full_name=p.student.full_name)
        )
    else:
        messages.success(
            request,
            f"{p.student.full_name} — “{p.title}”: " + (_("berildi, coin yechildi.") if approve else _("rad etildi.")),
        )
    return redirect(_back(request, p.student))


@login_required
def rewards(request, pk=None):
    """Coin do'koni: sovg'alar ro'yxati, qo'shish va tahrirlash."""
    reward = get_object_or_404(Reward, pk=pk) if pk else None
    form = RewardForm(request.POST or None, instance=reward)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, _("Sovg'a saqlandi."))
        return redirect("rewards")
    items = Reward.objects.annotate(
        given=Count("purchases", filter=Q(purchases__status=Purchase.Status.APPROVED)),
        waiting=Count("purchases", filter=Q(purchases__status=Purchase.Status.PENDING)),
    )
    return render(
        request,
        "academy/shop/rewards.html",
        {"form": form, "editing": reward, "rewards": items, "recent": Purchase.objects.select_related("student")[:15]},
    )
