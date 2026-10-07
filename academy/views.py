import csv
import random
import secrets
from datetime import date, timedelta
from urllib.parse import urlencode

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.cache import cache
from django.db import connection, transaction
from django.db.models import Avg, Count, Q, Sum
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_GET, require_POST
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    FormView,
    ListView,
    UpdateView,
)

from .forms import (
    GroupForm,
    LessonForm,
    LoginForm,
    ModuleForm,
    QuizForm,
    StudentForm,
    TopicForm,
    TopicImportForm,
)
from .models import (
    MAX_SCORE,
    Attendance,
    Group,
    Lesson,
    Module,
    Quiz,
    QuizAttempt,
    Student,
    SyllabusItem,
    Topic,
    new_attempt_token,
)
from .services import (
    dashboard_payload,
    ensure_quiz_attempts,
    export_topics,
    filter_students,
    group_journal,
    group_progress,
    groups_with_stats,
    import_topics,
    lesson_attendance_summary,
    percent,
    rating,
    sessions_between,
    start_session,
    student_attendance_rate,
    students_with_stats,
    week_start,
    week_timetable,
)


def int_param(request, name):
    """GET parametrini butun songa aylantiradi; noto'g'ri qiymat — None (500 emas)."""
    try:
        return int(request.GET.get(name, ""))
    except ValueError:
        return None


def choice_param(request, name, choices):
    value = request.GET.get(name, "")
    return value if value in choices.values else None


class AuthMixin(LoginRequiredMixin):
    pass


class DeleteMessageMixin:
    success_message = "O‘chirildi."

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)


def client_ip(request) -> str:
    if settings.TRUST_X_FORWARDED_FOR:
        # nginx `proxy_add_x_forwarded_for` mijoz manzilini oxiriga qo'shadi;
        # chapdagi qiymatlarni mijozning o'zi soxtalashtirishi mumkin.
        forwarded = request.META.get("HTTP_X_FORWARDED_FOR", "")
        if forwarded:
            return forwarded.split(",")[-1].strip()
    return request.META.get("REMOTE_ADDR", "")


class ThrottledLoginView(auth_views.LoginView):
    """Login: IP bo'yicha ketma-ket xato urinishlarni cheklaydi (brute-force himoyasi)."""

    template_name = "academy/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True

    def cache_key(self) -> str:
        return f"login-fail:{client_ip(self.request)}"

    def post(self, request, *args, **kwargs):
        if cache.get(self.cache_key(), 0) >= settings.LOGIN_FAILURE_LIMIT:
            # Bog'lanmagan forma: bloklangan paytda parol umuman tekshirilmaydi.
            form = self.get_form_class()(
                request, initial={"username": request.POST.get("username", "")}
            )
            context = self.get_context_data(form=form, locked_message=self.locked_message())
            return self.render_to_response(context, status=429)
        return super().post(request, *args, **kwargs)

    def form_invalid(self, form):
        key = self.cache_key()
        cache.add(key, 0, settings.LOGIN_LOCKOUT_SECONDS)
        try:
            failures = cache.incr(key)
        except ValueError:  # kalit shu orada muddati tugab o'chgan
            failures = 1
            cache.set(key, failures, settings.LOGIN_LOCKOUT_SECONDS)
        if failures >= settings.LOGIN_FAILURE_LIMIT:
            form.errors.pop("__all__", None)
            form.add_error(None, self.locked_message())
        return super().form_invalid(form)

    def form_valid(self, form):
        cache.delete(self.cache_key())
        return super().form_valid(form)

    def locked_message(self) -> str:
        minutes = max(1, settings.LOGIN_LOCKOUT_SECONDS // 60)
        return f"Juda ko‘p noto‘g‘ri urinish. {minutes} daqiqadan keyin qayta urinib ko‘ring."


@never_cache
@require_GET
def healthz(request):
    """Monitoring uchun: ilova va baza ishlayaptimi (login talab qilinmaydi)."""
    try:
        connection.ensure_connection()
    except Exception:  # har qanday baza xatosi — "ishlamayapti"
        return JsonResponse({"status": "error"}, status=503)
    return JsonResponse({"status": "ok"})


def csv_response(filename: str, header: list[str], rows) -> HttpResponse:
    """Excel'da to'g'ri ochiladigan CSV: UTF-8 BOM + ";" ajratuvchi."""
    response = HttpResponse(content_type="text/csv; charset=utf-8")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    response.write("﻿")
    writer = csv.writer(response, delimiter=";")
    writer.writerow(header)
    writer.writerows(rows)
    return response


@login_required
def dashboard(request):
    return render(request, "academy/dashboard.html", dashboard_payload())


@login_required
def timetable(request):
    """Haftalik dars jadvali. ?hafta=YYYY-MM-DD — shu sana tushgan hafta."""
    try:
        day = date.fromisoformat(request.GET.get("hafta", ""))
    except ValueError:
        day = timezone.localdate()
    ctx = week_timetable(week_start(day))
    ctx["unscheduled"] = Group.objects.filter(status=Group.Status.ACTIVE).filter(
        Q(days="") | Q(starts_at=None)
    )
    ctx["this_week"] = week_start(timezone.localdate())
    return render(request, "academy/timetable.html", ctx)


@login_required
@require_POST
def start_lesson(request, pk):
    """Jadvaldagi bugungi darsni bir bosishda boshlash va yo'qlamaga o'tish."""
    group = get_object_or_404(Group, pk=pk)
    lesson, created = start_session(group)
    if created:
        topic = lesson.topic.title if lesson.topic else "mavzusiz"
        messages.success(request, f"Dars boshlandi: {topic}. Yo‘qlamani belgilang.")
    return redirect("attendance", pk=lesson.pk)


# --- Guruhlar ---------------------------------------------------------------


class GroupListView(AuthMixin, ListView):
    model = Group
    template_name = "academy/groups/list.html"
    context_object_name = "groups"

    def get_queryset(self):
        qs = groups_with_stats()
        status = choice_param(self.request, "status", Group.Status)
        if status:
            qs = qs.filter(status=status)
        q = self.request.GET.get("q", "").strip()
        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(code__icontains=q))
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        today = timezone.localdate()
        scheduled = [
            g for g in ctx["groups"] if g.has_timetable and g.status == Group.Status.ACTIVE
        ]
        next_by_group = {}
        for session in sessions_between(today, today + timedelta(days=7), scheduled):
            if session.state in ("upcoming", "live"):
                next_by_group.setdefault(session.group.pk, session)
        for g in ctx["groups"]:
            g.next_session = next_by_group.get(g.pk)
            g.progress_pct = percent(g.syllabus_taught, g.syllabus_total)
        ctx["status_tabs"] = [("", "Barchasi"), *Group.Status.choices]
        return ctx


class GroupCreateView(AuthMixin, SuccessMessageMixin, CreateView):
    model = Group
    form_class = GroupForm
    template_name = "academy/groups/form.html"
    success_message = "Guruh yaratildi."


class GroupUpdateView(AuthMixin, SuccessMessageMixin, UpdateView):
    model = Group
    form_class = GroupForm
    template_name = "academy/groups/form.html"
    success_message = "Guruh yangilandi."


class GroupDeleteView(AuthMixin, DeleteMessageMixin, DeleteView):
    model = Group
    template_name = "academy/confirm_delete.html"
    success_url = reverse_lazy("group_list")
    success_message = "Guruh o‘chirildi."


class GroupDetailView(AuthMixin, DetailView):
    model = Group
    template_name = "academy/groups/detail.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        group = self.object
        in_syllabus = group.syllabus.values_list("topic_id", flat=True)
        today = timezone.localdate()
        students = list(
            students_with_stats(group.students.all()).annotate(score_avg=Avg("attendances__score"))
        )
        for s in students:
            s.att_pct = percent(s.att_present, s.att_total)
            s.score_avg = round(s.score_avg) if s.score_avg is not None else None
        ctx.update(
            progress=group_progress(group),
            students=students,
            sessions=(
                sessions_between(today, today + timedelta(days=21), [group])[:6]
                if group.has_timetable and group.status == Group.Status.ACTIVE
                else []
            ),
            syllabus=group.syllabus.select_related("topic", "topic__module"),
            lessons=group.lessons.select_related("topic")[:20],
            all_topics=Topic.objects.filter(is_active=True)
            .exclude(pk__in=in_syllabus)
            .select_related("module"),
            modules=Module.objects.annotate(
                free=Count(
                    "topics",
                    filter=Q(topics__is_active=True) & ~Q(topics__pk__in=in_syllabus),
                )
            ).filter(free__gt=0),
            next_item=group.next_syllabus_item(),
        )
        return ctx


JOURNAL_LIMIT = 30


@login_required
def group_journal_view(request, pk):
    group = get_object_or_404(Group, pk=pk)
    export = request.GET.get("format") == "csv"
    show_all = export or request.GET.get("all") == "1"
    lessons, rows = group_journal(group, limit=None if show_all else JOURNAL_LIMIT)

    if export:
        labels = dict(Attendance.Status.choices)

        def cell_text(cell):
            text = labels.get(cell.status, "")
            return f"{text} ({cell.score})" if cell.score is not None else text

        def blank_if_none(value):
            return "" if value is None else value

        header = [
            "F.I.Sh.",
            *(f"{lesson.held_on:%d.%m.%Y}" for lesson in lessons),
            "Keldi",
            "Belgilangan",
            "Davomat %",
            "O‘rtacha ball",
            "Reyting",
            "O‘rin",
        ]
        data = (
            [
                row.student.full_name,
                *(cell_text(cell) for cell in row.cells),
                row.attended,
                row.marked,
                row.percent,
                blank_if_none(row.avg_score),
                blank_if_none(row.rating),
                blank_if_none(row.rank),
            ]
            for row in rows
        )
        stamp = timezone.localdate().isoformat()
        return csv_response(f"jurnal-{group.code}-{stamp}.csv", header, data)

    return render(
        request,
        "academy/groups/journal.html",
        {
            "group": group,
            "lessons": lessons,
            "rows": rows,
            "show_all": show_all,
            "limit": JOURNAL_LIMIT,
        },
    )


@login_required
@require_POST
def add_syllabus_item(request, pk):
    group = get_object_or_404(Group, pk=pk)
    topic_id = request.POST.get("topic", "")
    module_id = request.POST.get("module", "")
    if module_id.isdigit():
        module = get_object_or_404(Module, pk=module_id)
        added = group.add_topics(module.topics.filter(is_active=True))
        messages.success(request, f"“{module}” bo‘limidan {added} ta mavzu qo‘shildi.")
    elif topic_id.isdigit():
        topic = get_object_or_404(Topic, pk=topic_id)
        if group.add_topics([topic]):
            messages.success(request, "Mavzu guruh dasturiga qo‘shildi.")
        else:
            messages.info(request, "Bu mavzu dasturda allaqachon bor.")
    else:
        messages.error(request, "Mavzu yoki bo‘lim tanlang.")
    return redirect(group.get_absolute_url())


@login_required
@require_POST
def toggle_syllabus(request, pk, item_id):
    item = get_object_or_404(
        SyllabusItem.objects.select_related("group"), pk=item_id, group_id=pk
    )
    group = item.group
    action = request.POST.get("action")
    if action == "taught":
        item.status = SyllabusItem.Status.TAUGHT
        item.taught_on = timezone.localdate()
    elif action == "planned":
        item.status = SyllabusItem.Status.PLANNED
        item.taught_on = None
    elif action == "skip":
        item.status = SyllabusItem.Status.SKIPPED
        item.taught_on = None
    elif action in ("up", "down"):
        item.move(action)
        return redirect(f"{group.get_absolute_url()}#syllabus-{item.pk}")
    elif action == "delete":
        item.delete()
        messages.success(request, "Mavzu dasturdan olib tashlandi.")
        return redirect(group.get_absolute_url())
    else:
        messages.error(request, "Noma’lum amal.")
        return redirect(group.get_absolute_url())
    item.save(update_fields=["status", "taught_on"])
    messages.success(request, "Dastur yangilandi.")
    return redirect(f"{group.get_absolute_url()}#syllabus-{item.pk}")


# --- Shogirdlar -------------------------------------------------------------


class StudentListView(AuthMixin, ListView):
    model = Student
    template_name = "academy/students/list.html"
    context_object_name = "students"
    paginate_by = 40

    def get_queryset(self):
        return students_with_stats(filter_students(self.request.GET))

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["groups"] = Group.objects.filter(status=Group.Status.ACTIVE)
        ctx["statuses"] = Student.Status.choices
        return ctx


@login_required
def student_export(request):
    """Shogirdlar CSV — ro'yxat sahifasidagi filtrlar bilan bir xil."""
    labels = dict(Student.Status.choices)
    rows = (
        [
            s.full_name,
            s.group.code,
            s.phone,
            f"@{s.telegram}" if s.telegram else "",
            labels.get(s.status, s.status),
            f"{s.joined_at:%d.%m.%Y}",
            percent(s.att_present, s.att_total) if s.att_total else "",
        ]
        for s in students_with_stats(filter_students(request.GET))
    )
    header = ["F.I.Sh.", "Guruh", "Telefon", "Telegram", "Holat", "Qo‘shilgan", "Davomat %"]
    stamp = timezone.localdate().isoformat()
    return csv_response(f"shogirdlar-{stamp}.csv", header, rows)


class StudentCreateView(AuthMixin, SuccessMessageMixin, CreateView):
    model = Student
    form_class = StudentForm
    template_name = "academy/students/form.html"
    success_message = "Shogird qo‘shildi."

    def get_initial(self):
        initial = super().get_initial()
        group = int_param(self.request, "group")
        if group:
            initial["group"] = group
        return initial

    def get_success_url(self):
        # "Saqlash va yana qo'shish" — guruhga ketma-ket shogird kiritish uchun.
        if "add_another" in self.request.POST:
            return f"{reverse('student_create')}?group={self.object.group_id}"
        return self.object.group.get_absolute_url()


class StudentUpdateView(AuthMixin, SuccessMessageMixin, UpdateView):
    model = Student
    form_class = StudentForm
    template_name = "academy/students/form.html"
    success_message = "Shogird yangilandi."


class StudentDeleteView(AuthMixin, DeleteMessageMixin, DeleteView):
    model = Student
    template_name = "academy/confirm_delete.html"
    success_url = reverse_lazy("student_list")
    success_message = "Shogird o‘chirildi."


class StudentDetailView(AuthMixin, DetailView):
    model = Student
    template_name = "academy/students/detail.html"

    def get_queryset(self):
        return Student.objects.select_related("group")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        rate = student_attendance_rate(self.object)
        history = list(
            self.object.attendances.select_related(
                "lesson", "lesson__topic", "lesson__group"
            ).order_by("-lesson__held_on")[:40]
        )
        ctx["rate"] = rate
        ctx["rating"] = rating(rate["avg_score"], rate["percent"]) if rate["total"] else None
        ctx["history"] = history
        ctx["timeline"] = history[:24][::-1]  # baho diagrammasi: eskisidan yangisiga
        ctx["quiz_attempts"] = self.object.quiz_attempts.select_related(
            "lesson", "quiz__topic"
        ).order_by("-lesson__held_on")[:20]
        return ctx


# --- Bo'limlar va mavzular --------------------------------------------------


class ModuleCreateView(AuthMixin, SuccessMessageMixin, CreateView):
    model = Module
    form_class = ModuleForm
    template_name = "academy/topics/module_form.html"
    success_message = "Bo‘lim yaratildi."


class ModuleUpdateView(AuthMixin, SuccessMessageMixin, UpdateView):
    model = Module
    form_class = ModuleForm
    template_name = "academy/topics/module_form.html"
    success_message = "Bo‘lim yangilandi."


class ModuleDeleteView(AuthMixin, DeleteMessageMixin, DeleteView):
    model = Module
    template_name = "academy/confirm_delete.html"
    success_url = reverse_lazy("topic_list")
    success_message = "Bo‘lim o‘chirildi. Uning mavzulari “bo‘limsiz” bo‘lib qoldi."


class TopicListView(AuthMixin, ListView):
    model = Topic
    template_name = "academy/topics/list.html"
    context_object_name = "topics"

    def get_queryset(self):
        qs = (
            Topic.objects.select_related("module", "quiz")
            .annotate(
                lesson_n=Count("lessons", distinct=True),
                group_n=Count("syllabus_items", distinct=True),
            )
            .order_by("order", "title")
        )
        q = self.request.GET.get("q", "").strip()
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q))
        module = self.request.GET.get("module", "")
        if module == "none":
            qs = qs.filter(module__isnull=True)
        elif module.isdigit():
            qs = qs.filter(module_id=module)
        if self.request.GET.get("hidden") != "1":
            qs = qs.filter(is_active=True)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # Mavzularni bo'lim bo'yicha guruhlash: [(module|None, [topics]), ...]
        sections: dict = {}
        for t in ctx["topics"]:
            sections.setdefault(t.module, []).append(t)
        ctx["sections"] = sorted(
            sections.items(),
            key=lambda kv: (kv[0] is None, kv[0].order if kv[0] else 0, str(kv[0])),
        )
        ctx["modules"] = Module.objects.annotate(topic_n=Count("topics"))
        ctx["hidden_n"] = Topic.objects.filter(is_active=False).count()
        return ctx


class TopicDetailView(AuthMixin, DetailView):
    model = Topic
    template_name = "academy/topics/detail.html"

    def get_queryset(self):
        return Topic.objects.select_related("module")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        topic = self.object
        ctx["syllabus_items"] = topic.syllabus_items.select_related("group")
        ctx["lessons"] = topic.lessons.select_related("group")[:20]
        quiz = getattr(topic, "quiz", None)
        if quiz:
            ctx["quiz"] = quiz
            ctx["question_n"] = quiz.questions.count()
            ctx["quiz_stats"] = quiz.attempts.filter(
                status=QuizAttempt.Status.FINISHED
            ).aggregate(n=Count("pk"), correct=Sum("correct"), total=Sum("total"))
            stats = ctx["quiz_stats"]
            stats["avg"] = percent(stats["correct"] or 0, stats["total"] or 0)
        siblings = list(
            Topic.objects.filter(module_id=topic.module_id, is_active=True)
            .order_by("order", "title")
            .values_list("pk", flat=True)
        )
        if topic.pk in siblings:
            i = siblings.index(topic.pk)
            ctx["prev_id"] = siblings[i - 1] if i > 0 else None
            ctx["next_id"] = siblings[i + 1] if i + 1 < len(siblings) else None
        return ctx


class TopicCreateView(AuthMixin, SuccessMessageMixin, CreateView):
    model = Topic
    form_class = TopicForm
    template_name = "academy/topics/form.html"
    success_message = "Mavzu qo‘shildi."

    def get_initial(self):
        initial = super().get_initial()
        module = int_param(self.request, "module")
        if module:
            initial["module"] = module
        return initial


class TopicUpdateView(AuthMixin, SuccessMessageMixin, UpdateView):
    model = Topic
    form_class = TopicForm
    template_name = "academy/topics/form.html"
    success_message = "Mavzu yangilandi."


class TopicDeleteView(AuthMixin, DeleteMessageMixin, DeleteView):
    model = Topic
    template_name = "academy/confirm_delete.html"
    success_url = reverse_lazy("topic_list")
    success_message = "Mavzu o‘chirildi."


class TopicImportView(AuthMixin, FormView):
    """Ikki bosqichli import: avval ko'rib chiqish, keyin tasdiqlash."""

    form_class = TopicImportForm
    template_name = "academy/topics/import.html"

    def form_valid(self, form):
        if self.request.POST.get("confirm") != "1":
            return self.render_to_response(
                self.get_context_data(form=form, preview=form.parsed)
            )
        result = import_topics(
            form.parsed,
            groups=form.cleaned_data["groups"],
            default_duration=form.cleaned_data["default_duration"],
        )
        parts = [
            f"{result.topics_created} ta yangi mavzu",
            f"{result.modules_created} ta yangi bo‘lim",
        ]
        if result.topics_updated:
            parts.append(f"{result.topics_updated} ta mavzu yangilandi")
        if result.added_to_groups:
            parts.append(f"guruh dasturlariga {result.added_to_groups} ta yozuv")
        messages.success(self.request, "Import tayyor: " + ", ".join(parts) + ".")
        return redirect("topic_list")


@login_required
def topic_export(request):
    response = HttpResponse(export_topics(), content_type="text/plain; charset=utf-8")
    stamp = timezone.localdate().isoformat()
    response["Content-Disposition"] = f'attachment; filename="mavzular-{stamp}.txt"'
    return response


# --- Darslar ----------------------------------------------------------------


class LessonListView(AuthMixin, ListView):
    model = Lesson
    template_name = "academy/lessons/list.html"
    context_object_name = "lessons"
    paginate_by = 30

    def get_queryset(self):
        # Count() bilan Meta.ordering qo'llanmaydi — tartibni aniq beramiz.
        qs = (
            Lesson.objects.select_related("group", "topic")
            .annotate(marked=Count("attendances"))
            .order_by(*Lesson._meta.ordering)
        )
        group = int_param(self.request, "group")
        status = choice_param(self.request, "status", Lesson.Status)
        if group:
            qs = qs.filter(group_id=group)
        if status:
            qs = qs.filter(status=status)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["groups"] = Group.objects.filter(status=Group.Status.ACTIVE)
        ctx["statuses"] = Lesson.Status.choices
        ctx["today"] = timezone.localdate()
        return ctx


class LessonCreateView(AuthMixin, SuccessMessageMixin, CreateView):
    model = Lesson
    form_class = LessonForm
    template_name = "academy/lessons/form.html"
    success_message = "Dars yozildi."

    def get_initial(self):
        initial = super().get_initial()
        try:
            initial["held_on"] = date.fromisoformat(self.request.GET.get("sana", ""))
        except ValueError:
            initial["held_on"] = timezone.localdate()
        group_id = int_param(self.request, "group")
        topic_id = int_param(self.request, "topic")
        if group_id:
            initial["group"] = group_id
            group = Group.objects.filter(pk=group_id).first()
            if group and group.starts_at:
                initial["starts_at"] = group.starts_at
            next_item = group.next_syllabus_item() if group else None
            if next_item and not topic_id:
                # Guruh dasturidagi navbatdagi mavzuni taklif qilamiz.
                initial["topic"] = next_item.topic_id
        if topic_id:
            initial["topic"] = topic_id
        return initial


class LessonUpdateView(AuthMixin, SuccessMessageMixin, UpdateView):
    model = Lesson
    form_class = LessonForm
    template_name = "academy/lessons/form.html"
    success_message = "Dars yangilandi."


class LessonDeleteView(AuthMixin, DeleteMessageMixin, DeleteView):
    model = Lesson
    template_name = "academy/confirm_delete.html"
    success_url = reverse_lazy("lesson_list")
    success_message = "Dars o‘chirildi."


class LessonDetailView(AuthMixin, DetailView):
    model = Lesson
    template_name = "academy/lessons/detail.html"

    def get_queryset(self):
        return Lesson.objects.select_related("group", "topic", "topic__module")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        lesson = self.object
        ctx["summary"] = lesson_attendance_summary(lesson)
        ctx["attendances"] = lesson.attendances.select_related("student")
        ctx["quiz"] = getattr(lesson.topic, "quiz", None)
        if ctx["quiz"]:
            finalize_expired_attempts(lesson.quiz_attempts.all())
            attempts = list(lesson.quiz_attempts.select_related("student", "quiz__topic"))
            for a in attempts:
                a.link = self.request.build_absolute_uri(a.get_absolute_url())
                a.share_url = telegram_share_url(a.link, a)
            ctx["attempts"] = attempts
            finished = [a for a in attempts if a.status == QuizAttempt.Status.FINISHED]
            ctx["quiz_finished"] = len(finished)
            ctx["quiz_avg"] = (
                round(sum(a.percent for a in finished) / len(finished)) if finished else None
            )
            ctx["links_text"] = "\n".join(f"{a.student.full_name}: {a.link}" for a in attempts)
        return ctx


@login_required
@require_POST
def complete_lesson(request, pk):
    lesson = get_object_or_404(Lesson.objects.select_related("topic"), pk=pk)
    lesson.mark_completed()
    message = "Dars o‘tildi deb belgilandi. Mavzu dasturda yangilandi."
    if hasattr(lesson.topic, "quiz"):
        message += " Endi shogirdlarga test havolalarini yuboring."
        messages.success(request, message)
        return redirect(f"{lesson.get_absolute_url()}#quiz")
    messages.success(request, message)
    return redirect(lesson.get_absolute_url())


def parse_score(raw: str) -> tuple[int | None, bool]:
    """Formadagi ballni o'qiydi: (qiymat, to'g'rimi). Bo'sh — baholanmagan."""
    raw = raw.strip()
    if not raw:
        return None, True
    if raw.isdigit() and int(raw) <= MAX_SCORE:
        return int(raw), True
    return None, False


@login_required
def attendance_sheet(request, pk):
    lesson = get_object_or_404(
        Lesson.objects.select_related("group", "topic"), pk=pk
    )
    existing = {a.student_id: a for a in lesson.attendances.all()}
    # Faol shogirdlar + avval belgilangan (keyin ketgan bo'lsa ham) shogirdlar.
    students = lesson.group.students.filter(
        Q(status=Student.Status.ACTIVE) | Q(pk__in=list(existing))
    )

    if request.method == "POST":
        bad_scores = []
        with transaction.atomic():
            for student in students:
                status = request.POST.get(f"status_{student.pk}")
                if status not in Attendance.Status.values:
                    continue
                note = request.POST.get(f"note_{student.pk}", "").strip()[:200]
                score, ok = parse_score(request.POST.get(f"score_{student.pk}", ""))
                if not ok:
                    bad_scores.append(student.full_name)
                    # Noto'g'ri kiritilgan ball avvalgi qiymatni o'chirib yubormasin.
                    score = existing[student.pk].score if student.pk in existing else None
                Attendance.objects.update_or_create(
                    lesson=lesson,
                    student=student,
                    defaults={"status": status, "note": note, "score": score},
                )
            if request.POST.get("complete") == "1":
                lesson.mark_completed()
        if bad_scores:
            messages.warning(
                request,
                f"Ball 0 dan {MAX_SCORE} gacha butun son bo‘lishi kerak — saqlanmadi: "
                + ", ".join(bad_scores),
            )
        if request.POST.get("complete") == "1":
            messages.success(request, "Yo‘qlama saqlandi va dars o‘tildi deb belgilandi.")
            return redirect(lesson.get_absolute_url())
        messages.success(request, "Yo‘qlama saqlandi.")
        return redirect("attendance", pk=lesson.pk)

    rows = []
    for student in students:
        rec = existing.get(student.pk)
        rows.append(
            {
                "student": student,
                "status": rec.status if rec else Attendance.Status.PRESENT,
                "note": rec.note if rec else "",
                "score": rec.score if rec else None,
            }
        )
    return render(
        request,
        "academy/lessons/attendance.html",
        {
            "lesson": lesson,
            "rows": rows,
            "statuses": Attendance.Status.choices,
            "summary": lesson_attendance_summary(lesson),
            "is_saved": bool(existing),
        },
    )


@login_required
def search(request):
    q = (request.GET.get("q") or "").strip()
    students = groups = lessons = topics = []
    if q:
        students = Student.objects.filter(
            Q(full_name__icontains=q)
            | Q(phone__icontains=q)
            | Q(telegram__icontains=q.lstrip("@"))
        ).select_related("group")[:8]
        groups = Group.objects.filter(Q(name__icontains=q) | Q(code__icontains=q))[:6]
        topics = Topic.objects.filter(
            Q(title__icontains=q) | Q(description__icontains=q)
        ).select_related("module")[:8]
        lessons = Lesson.objects.filter(
            Q(topic__title__icontains=q) | Q(notes__icontains=q) | Q(homework__icontains=q)
        ).select_related("group", "topic")[:6]
    if request.GET.get("format") == "json":
        # Buyruqlar paneli (Ctrl+K) uchun ixcham natija.
        def hit(kind, title, meta, url):
            return {"kind": kind, "title": title, "meta": meta, "url": url}

        results = [
            *(hit("student", s.full_name, s.group.code, s.get_absolute_url()) for s in students),
            *(hit("group", g.name, g.schedule or g.code, g.get_absolute_url()) for g in groups),
            *(
                hit("topic", t.title, t.module.title if t.module else "", t.get_absolute_url())
                for t in topics
            ),
            *(
                hit(
                    "lesson",
                    lesson.topic.title if lesson.topic else "Mavzusiz dars",
                    f"{lesson.group.code} · {lesson.held_on:%d.%m.%Y}",
                    lesson.get_absolute_url(),
                )
                for lesson in lessons
            ),
        ]
        return JsonResponse({"q": q, "results": results})
    return render(
        request,
        "academy/search.html",
        {
            "q": q,
            "students": students,
            "groups": groups,
            "topics": topics,
            "lessons": lessons,
        },
    )


# --- Testlar (o'qituvchi) ---------------------------------------------------


@login_required
def quiz_edit(request, pk):
    topic = get_object_or_404(Topic, pk=pk)
    quiz = getattr(topic, "quiz", None) or Quiz(topic=topic)
    form = QuizForm(request.POST or None, instance=quiz)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, f"Test saqlandi: {len(form.parsed)} ta savol.")
        return redirect(f"{topic.get_absolute_url()}#quiz")
    return render(request, "academy/quiz/form.html", {"form": form, "topic": topic})


class QuizDeleteView(AuthMixin, DeleteMessageMixin, DeleteView):
    model = Quiz
    template_name = "academy/confirm_delete.html"
    success_message = "Test o‘chirildi."

    def get_object(self, queryset=None):
        return get_object_or_404(Quiz.objects.select_related("topic"), topic_id=self.kwargs["pk"])

    def get_success_url(self):
        return self.object.topic.get_absolute_url()


def finalize_expired_attempts(qs) -> None:
    """Vaqti tugagan, lekin yakunlanmagan (sahifa yopilgan) testlarni baholaydi."""
    cutoff = timezone.now() - timedelta(seconds=QuizAttempt.GRACE_SECONDS)
    for attempt in qs.filter(status=QuizAttempt.Status.ACTIVE, deadline__lt=cutoff):
        attempt.finish(timed_out=True)


def telegram_share_url(link: str, attempt: QuizAttempt) -> str:
    text = (
        f"{attempt.student.full_name}, “{attempt.quiz.topic.title}” mavzusi bo‘yicha test. "
        f"Vaqt: {attempt.quiz.time_limit_minutes} daqiqa. Havola faqat bir marta ishlaydi."
    )
    return "https://t.me/share/url?" + urlencode({"url": link, "text": text})


@login_required
@require_POST
def lesson_quiz_links(request, pk):
    lesson = get_object_or_404(Lesson.objects.select_related("group", "topic"), pk=pk)
    if not hasattr(lesson.topic, "quiz"):
        messages.error(request, "Bu dars mavzusida test yo‘q. Avval mavzuga test yarating.")
        return redirect(lesson.get_absolute_url())
    created = ensure_quiz_attempts(lesson)
    if created:
        messages.success(request, f"{created} ta shogird uchun test havolasi yaratildi.")
    else:
        messages.info(request, "Barcha faol shogirdlarda havola allaqachon bor.")
    return redirect(f"{lesson.get_absolute_url()}#quiz")


@login_required
@require_POST
def quiz_attempt_renew(request, pk):
    """Yakunlanmagan havolani yangisiga almashtiradi (eski havola ishlamay qoladi)."""
    attempt = get_object_or_404(QuizAttempt.objects.select_related("lesson"), pk=pk)
    if attempt.status == QuizAttempt.Status.FINISHED:
        messages.error(request, "Test yakunlangan — natijani o‘chirib bo‘lmaydi.")
    else:
        attempt.token = new_attempt_token()
        attempt.status = QuizAttempt.Status.PENDING
        attempt.owner_key = ""
        attempt.answers = {}
        attempt.started_at = attempt.deadline = None
        attempt.save()
        messages.success(request, f"{attempt.student} uchun yangi havola yaratildi.")
    return redirect(f"{attempt.lesson.get_absolute_url()}#quiz")


# --- Testlar (o'quvchi, login talab qilinmaydi) -----------------------------


def _owner_cookie(attempt: QuizAttempt) -> str:
    return f"quiz_{attempt.pk}"


def _is_owner(request, attempt: QuizAttempt) -> bool:
    key = request.COOKIES.get(_owner_cookie(attempt), "")
    return bool(key and attempt.owner_key) and secrets.compare_digest(key, attempt.owner_key)


def _shuffled_questions(attempt: QuizAttempt) -> list:
    """Savollar va variantlar har bir o'quvchida o'z tartibida (urug' — token)."""
    rng = random.Random(attempt.token)
    questions = list(attempt.quiz.questions.prefetch_related("choices"))
    rng.shuffle(questions)
    for q in questions:
        q.shuffled = list(q.choices.all())
        rng.shuffle(q.shuffled)
        q.picked = attempt.answers.get(str(q.pk))
    return questions


def _posted_answers(request, attempt: QuizAttempt) -> dict:
    answers = {}
    for qid in attempt.quiz.questions.values_list("pk", flat=True):
        value = request.POST.get(f"q{qid}", "")
        if value.isdigit():
            answers[str(qid)] = int(value)
    return answers


def _quiz_page(request, attempt, template, status=200, **extra):
    response = render(
        request,
        f"academy/quiz/{template}.html",
        {"attempt": attempt, "quiz": attempt.quiz, "topic": attempt.quiz.topic, **extra},
        status=status,
    )
    response["X-Robots-Tag"] = "noindex, nofollow"
    return response


@never_cache
def quiz_take(request, token):
    attempt = get_object_or_404(
        QuizAttempt.objects.select_related("quiz__topic", "student"), token=token
    )
    owner = _is_owner(request, attempt)
    Status = QuizAttempt.Status

    if attempt.status == Status.ACTIVE and attempt.is_expired(grace=QuizAttempt.GRACE_SECONDS):
        attempt.finish(timed_out=True)

    if attempt.status == Status.FINISHED:
        if owner:
            return _quiz_page(request, attempt, "result")
        return _quiz_page(request, attempt, "used", status=410)

    if attempt.status == Status.ACTIVE:
        if not owner:
            return _quiz_page(request, attempt, "used", status=410)
        return _quiz_page(
            request,
            attempt,
            "take",
            questions=_shuffled_questions(attempt),
            seconds_left=attempt.seconds_left(),
        )

    # Ochilmagan havola: GET faqat kirish sahifasini ko'rsatadi. Telegram havolaning
    # oldindan ko'rinishi (preview) uchun uni o'zi ochadi — bu testni "yoqib" yubormasin.
    if request.method != "POST":
        return _quiz_page(request, attempt, "start", question_n=attempt.quiz.questions.count())
    owner_key = secrets.token_urlsafe(24)
    if not attempt.start(owner_key):
        return _quiz_page(request, attempt, "used", status=410)
    response = redirect(attempt.get_absolute_url())
    response.set_cookie(
        _owner_cookie(attempt),
        owner_key,
        max_age=attempt.quiz.time_limit_minutes * 60 + 7 * 24 * 3600,
        path=attempt.get_absolute_url(),
        secure=request.is_secure(),
        httponly=True,
        samesite="Lax",
    )
    return response


@never_cache
@require_POST
def quiz_save(request, token):
    """Javoblarni oraliq saqlash (JS): sahifa yopilsa ham vaqt tugaganda baholanadi."""
    attempt = get_object_or_404(QuizAttempt.objects.select_related("quiz"), token=token)
    if (
        attempt.status != QuizAttempt.Status.ACTIVE
        or not _is_owner(request, attempt)
        or attempt.is_expired(grace=QuizAttempt.GRACE_SECONDS)
    ):
        return JsonResponse({"ok": False}, status=409)
    attempt.answers = _posted_answers(request, attempt)
    attempt.save(update_fields=["answers"])
    return JsonResponse({"ok": True, "seconds_left": attempt.seconds_left()})


@never_cache
@require_POST
def quiz_submit(request, token):
    attempt = get_object_or_404(QuizAttempt.objects.select_related("quiz"), token=token)
    if attempt.status == QuizAttempt.Status.ACTIVE and _is_owner(request, attempt):
        if attempt.is_expired(grace=QuizAttempt.GRACE_SECONDS):
            # Juda kech yuborilgan javoblar qabul qilinmaydi — oxirgi saqlangani baholanadi.
            attempt.finish(timed_out=True)
        else:
            attempt.finish(
                _posted_answers(request, attempt),
                timed_out=request.POST.get("timeout") == "1" or attempt.is_expired(),
            )
    return redirect(attempt.get_absolute_url())
