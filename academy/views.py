from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.db.models import Count, Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.decorators.http import require_POST
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
    ModuleForm,
    StudentForm,
    TopicForm,
    TopicImportForm,
)
from .models import Attendance, Group, Lesson, Module, Student, SyllabusItem, Topic
from .services import (
    dashboard_payload,
    export_topics,
    group_progress,
    groups_with_stats,
    import_topics,
    lesson_attendance_summary,
    student_attendance_rate,
    students_with_stats,
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


@login_required
def dashboard(request):
    return render(request, "academy/dashboard.html", dashboard_payload())


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
        ctx.update(
            progress=group_progress(group),
            students=group.students.all(),
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
        qs = students_with_stats(Student.objects.select_related("group"))
        group = int_param(self.request, "group")
        status = choice_param(self.request, "status", Student.Status)
        q = self.request.GET.get("q", "").strip()
        if group:
            qs = qs.filter(group_id=group)
        if status:
            qs = qs.filter(status=status)
        if q:
            qs = qs.filter(
                Q(full_name__icontains=q)
                | Q(phone__icontains=q)
                | Q(telegram__icontains=q.lstrip("@"))
            )
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["groups"] = Group.objects.filter(status=Group.Status.ACTIVE)
        ctx["statuses"] = Student.Status.choices
        return ctx


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
        ctx["rate"] = student_attendance_rate(self.object)
        ctx["history"] = self.object.attendances.select_related(
            "lesson", "lesson__topic", "lesson__group"
        ).order_by("-lesson__held_on")[:40]
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
            Topic.objects.select_related("module")
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
        initial["held_on"] = timezone.localdate()
        group_id = int_param(self.request, "group")
        topic_id = int_param(self.request, "topic")
        if group_id:
            initial["group"] = group_id
            group = Group.objects.filter(pk=group_id).first()
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
        ctx["summary"] = lesson_attendance_summary(self.object)
        ctx["attendances"] = self.object.attendances.select_related("student")
        return ctx


@login_required
@require_POST
def complete_lesson(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    lesson.mark_completed()
    messages.success(request, "Dars o‘tildi deb belgilandi. Mavzu dasturda yangilandi.")
    return redirect(lesson.get_absolute_url())


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
        with transaction.atomic():
            for student in students:
                status = request.POST.get(f"status_{student.pk}")
                if status not in Attendance.Status.values:
                    continue
                note = request.POST.get(f"note_{student.pk}", "").strip()[:200]
                Attendance.objects.update_or_create(
                    lesson=lesson,
                    student=student,
                    defaults={"status": status, "note": note},
                )
            if request.POST.get("complete") == "1":
                lesson.mark_completed()
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
            Q(full_name__icontains=q) | Q(phone__icontains=q) | Q(telegram__icontains=q)
        ).select_related("group")[:8]
        groups = Group.objects.filter(Q(name__icontains=q) | Q(code__icontains=q))[:6]
        topics = Topic.objects.filter(
            Q(title__icontains=q) | Q(description__icontains=q)
        ).select_related("module")[:8]
        lessons = Lesson.objects.filter(
            Q(topic__title__icontains=q) | Q(notes__icontains=q) | Q(homework__icontains=q)
        ).select_related("group", "topic")[:6]
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
