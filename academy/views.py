from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import GroupForm, LessonForm, StudentForm, TopicForm
from .models import Attendance, Group, Lesson, Student, SyllabusItem, Topic
from .services import (
    dashboard_payload,
    group_progress,
    lesson_attendance_summary,
    student_attendance_rate,
)


class AuthMixin(LoginRequiredMixin):
    login_url = reverse_lazy("login")


@login_required
def dashboard(request):
    return render(request, "academy/dashboard.html", dashboard_payload())


class GroupListView(AuthMixin, ListView):
    model = Group
    template_name = "academy/groups/list.html"
    context_object_name = "groups"

    def get_queryset(self):
        qs = Group.objects.annotate(
            student_n=Count(
                "students", filter=Q(students__status=Student.Status.ACTIVE)
            )
        )
        status = self.request.GET.get("status")
        if status:
            qs = qs.filter(status=status)
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(code__icontains=q))
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        return ctx


class GroupCreateView(AuthMixin, CreateView):
    model = Group
    form_class = GroupForm
    template_name = "academy/groups/form.html"

    def form_valid(self, form):
        messages.success(self.request, "Guruh yaratildi.")
        return super().form_valid(form)


class GroupUpdateView(AuthMixin, UpdateView):
    model = Group
    form_class = GroupForm
    template_name = "academy/groups/form.html"

    def form_valid(self, form):
        messages.success(self.request, "Guruh yangilandi.")
        return super().form_valid(form)


class GroupDeleteView(AuthMixin, DeleteView):
    model = Group
    template_name = "academy/confirm_delete.html"
    success_url = reverse_lazy("group_list")

    def form_valid(self, form):
        messages.success(self.request, "Guruh o'chirildi.")
        return super().form_valid(form)


class GroupDetailView(AuthMixin, DetailView):
    model = Group
    template_name = "academy/groups/detail.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        group = self.object
        ctx["progress"] = group_progress(group)
        ctx["students"] = group.students.all()
        ctx["syllabus"] = group.syllabus.select_related("topic")
        ctx["lessons"] = group.lessons.select_related("topic")[:20]
        ctx["all_topics"] = Topic.objects.filter(is_active=True).exclude(
            pk__in=group.syllabus.values_list("topic_id", flat=True)
        )
        return ctx


@login_required
def add_syllabus_item(request, pk):
    group = get_object_or_404(Group, pk=pk)
    if request.method == "POST":
        topic_id = request.POST.get("topic")
        topic = get_object_or_404(Topic, pk=topic_id)
        last = group.syllabus.order_by("-order").first()
        order = (last.order + 1) if last else 1
        SyllabusItem.objects.get_or_create(
            group=group, topic=topic, defaults={"order": order}
        )
        messages.success(request, "Mavzu guruh dasturiga qo‘shildi.")
    return redirect(group.get_absolute_url())


@login_required
def toggle_syllabus(request, pk, item_id):
    group = get_object_or_404(Group, pk=pk)
    item = get_object_or_404(SyllabusItem, pk=item_id, group=group)
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "taught":
            item.status = SyllabusItem.Status.TAUGHT
            item.taught_on = timezone.localdate()
        elif action == "planned":
            item.status = SyllabusItem.Status.PLANNED
            item.taught_on = None
        elif action == "skip":
            item.status = SyllabusItem.Status.SKIPPED
        elif action == "delete":
            item.delete()
            messages.success(request, "Mavzu dasturdan olib tashlandi.")
            return redirect(group.get_absolute_url())
        item.save()
        messages.success(request, "Dastur yangilandi.")
    return redirect(group.get_absolute_url())


class StudentListView(AuthMixin, ListView):
    model = Student
    template_name = "academy/students/list.html"
    context_object_name = "students"
    paginate_by = 40

    def get_queryset(self):
        qs = Student.objects.select_related("group")
        group = self.request.GET.get("group")
        status = self.request.GET.get("status")
        q = self.request.GET.get("q")
        if group:
            qs = qs.filter(group_id=group)
        if status:
            qs = qs.filter(status=status)
        if q:
            qs = qs.filter(
                Q(full_name__icontains=q)
                | Q(phone__icontains=q)
                | Q(telegram__icontains=q)
            )
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["groups"] = Group.objects.filter(status=Group.Status.ACTIVE)
        return ctx


class StudentCreateView(AuthMixin, CreateView):
    model = Student
    form_class = StudentForm
    template_name = "academy/students/form.html"
    success_url = reverse_lazy("student_list")

    def get_initial(self):
        initial = super().get_initial()
        if self.request.GET.get("group"):
            initial["group"] = self.request.GET["group"]
        return initial

    def form_valid(self, form):
        messages.success(self.request, "Shogird qo‘shildi.")
        return super().form_valid(form)


class StudentUpdateView(AuthMixin, UpdateView):
    model = Student
    form_class = StudentForm
    template_name = "academy/students/form.html"

    def form_valid(self, form):
        messages.success(self.request, "Shogird yangilandi.")
        return super().form_valid(form)


class StudentDeleteView(AuthMixin, DeleteView):
    model = Student
    template_name = "academy/confirm_delete.html"
    success_url = reverse_lazy("student_list")

    def form_valid(self, form):
        messages.success(self.request, "Shogird o‘chirildi.")
        return super().form_valid(form)


class StudentDetailView(AuthMixin, DetailView):
    model = Student
    template_name = "academy/students/detail.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["rate"] = student_attendance_rate(self.object)
        ctx["history"] = self.object.attendances.select_related(
            "lesson", "lesson__topic", "lesson__group"
        ).order_by("-lesson__held_on")[:40]
        return ctx


class TopicListView(AuthMixin, ListView):
    model = Topic
    template_name = "academy/topics/list.html"
    context_object_name = "topics"

    def get_queryset(self):
        qs = Topic.objects.annotate(lesson_n=Count("lessons"))
        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(title__icontains=q)
        return qs


class TopicCreateView(AuthMixin, CreateView):
    model = Topic
    form_class = TopicForm
    template_name = "academy/topics/form.html"
    success_url = reverse_lazy("topic_list")

    def form_valid(self, form):
        messages.success(self.request, "Mavzu qo‘shildi.")
        return super().form_valid(form)


class TopicUpdateView(AuthMixin, UpdateView):
    model = Topic
    form_class = TopicForm
    template_name = "academy/topics/form.html"
    success_url = reverse_lazy("topic_list")

    def form_valid(self, form):
        messages.success(self.request, "Mavzu yangilandi.")
        return super().form_valid(form)


class TopicDeleteView(AuthMixin, DeleteView):
    model = Topic
    template_name = "academy/confirm_delete.html"
    success_url = reverse_lazy("topic_list")


class LessonListView(AuthMixin, ListView):
    model = Lesson
    template_name = "academy/lessons/list.html"
    context_object_name = "lessons"
    paginate_by = 30

    def get_queryset(self):
        qs = Lesson.objects.select_related("group", "topic")
        group = self.request.GET.get("group")
        status = self.request.GET.get("status")
        if group:
            qs = qs.filter(group_id=group)
        if status:
            qs = qs.filter(status=status)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["groups"] = Group.objects.filter(status=Group.Status.ACTIVE)
        return ctx


class LessonCreateView(AuthMixin, CreateView):
    model = Lesson
    form_class = LessonForm
    template_name = "academy/lessons/form.html"

    def get_initial(self):
        initial = super().get_initial()
        initial["held_on"] = timezone.localdate()
        if self.request.GET.get("group"):
            initial["group"] = self.request.GET["group"]
        if self.request.GET.get("topic"):
            initial["topic"] = self.request.GET["topic"]
        return initial

    def form_valid(self, form):
        messages.success(self.request, "Dars yozildi.")
        response = super().form_valid(form)
        if self.object.status == Lesson.Status.COMPLETED:
            self.object.mark_completed()
        return response


class LessonUpdateView(AuthMixin, UpdateView):
    model = Lesson
    form_class = LessonForm
    template_name = "academy/lessons/form.html"

    def form_valid(self, form):
        messages.success(self.request, "Dars yangilandi.")
        return super().form_valid(form)


class LessonDeleteView(AuthMixin, DeleteView):
    model = Lesson
    template_name = "academy/confirm_delete.html"
    success_url = reverse_lazy("lesson_list")


class LessonDetailView(AuthMixin, DetailView):
    model = Lesson
    template_name = "academy/lessons/detail.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["summary"] = lesson_attendance_summary(self.object)
        ctx["attendances"] = self.object.attendances.select_related("student")
        return ctx


@login_required
def complete_lesson(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    if request.method == "POST":
        lesson.mark_completed()
        messages.success(request, "Dars o‘tildi deb belgilandi. Mavzu dasturda yangilandi.")
    return redirect(lesson.get_absolute_url())


@login_required
def attendance_sheet(request, pk):
    lesson = get_object_or_404(
        Lesson.objects.select_related("group", "topic"), pk=pk
    )
    students = lesson.group.students.filter(status=Student.Status.ACTIVE)
    existing = {
        a.student_id: a for a in lesson.attendances.select_related("student")
    }

    if request.method == "POST":
        for student in students:
            status = request.POST.get(f"status_{student.pk}")
            note = request.POST.get(f"note_{student.pk}", "").strip()
            if status not in Attendance.Status.values:
                continue
            Attendance.objects.update_or_create(
                lesson=lesson,
                student=student,
                defaults={"status": status, "note": note},
            )
        if request.POST.get("complete") == "1":
            lesson.mark_completed()
            messages.success(
                request, "Yo‘qlama saqlandi va dars o‘tildi deb belgilandi."
            )
        else:
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
        },
    )


@login_required
def search(request):
    q = (request.GET.get("q") or "").strip()
    students = groups = lessons = topics = []
    if q:
        students = Student.objects.filter(full_name__icontains=q).select_related(
            "group"
        )[:8]
        groups = Group.objects.filter(
            Q(name__icontains=q) | Q(code__icontains=q)
        )[:6]
        topics = Topic.objects.filter(title__icontains=q)[:6]
        lessons = Lesson.objects.filter(
            Q(topic__title__icontains=q) | Q(notes__icontains=q)
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
