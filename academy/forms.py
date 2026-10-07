from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q

from .models import WEEKDAY_CHOICES, Group, Lesson, Module, Quiz, Student, Topic
from .services import QUIZ_FORMAT_HELP, parse_quiz, parse_topics


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {"class": "input", "placeholder": "Login", "autofocus": True}
        )
        self.fields["password"].widget.attrs.update(
            {"class": "input", "placeholder": "Parol"}
        )
        self.fields["username"].label = "Login"
        self.fields["password"].label = "Parol"


class StyledFormMixin:
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("label_suffix", "")  # "Nomi:" emas, "Nomi"
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            widget = field.widget
            if isinstance(widget, (forms.CheckboxInput, forms.CheckboxSelectMultiple)):
                widget.attrs.setdefault("class", "check")
                continue
            widget.attrs.setdefault("class", "input")
            if isinstance(widget, forms.Textarea):
                widget.attrs.setdefault("rows", 4)
            if field.required and not widget.attrs.get("placeholder"):
                widget.attrs.setdefault("placeholder", field.label or name)


class GroupForm(StyledFormMixin, forms.ModelForm):
    days = forms.TypedMultipleChoiceField(
        label="Dars kunlari",
        choices=WEEKDAY_CHOICES,
        coerce=int,
        widget=forms.CheckboxSelectMultiple(attrs={"class": "check"}),
        required=False,
    )

    class Meta:
        model = Group
        fields = [
            "name",
            "code",
            "days",
            "starts_at",
            "ends_at",
            "room",
            "start_date",
            "status",
            "notes",
        ]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "starts_at": forms.TimeInput(attrs={"type": "time"}, format="%H:%M"),
            "ends_at": forms.TimeInput(attrs={"type": "time"}, format="%H:%M"),
            "notes": forms.Textarea(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.initial["days"] = self.instance.day_list

    def clean_code(self):
        return self.cleaned_data["code"].strip().upper()

    def clean_days(self):
        return ",".join(str(d) for d in sorted(set(self.cleaned_data["days"])))

    def clean(self):
        cleaned = super().clean()
        days, starts, ends = cleaned.get("days"), cleaned.get("starts_at"), cleaned.get("ends_at")
        if days and not starts:
            self.add_error("starts_at", "Dars kunlari tanlangan — boshlanish vaqtini kiriting.")
        if starts and ends and ends <= starts:
            self.add_error("ends_at", "Tugash vaqti boshlanishidan keyin bo‘lishi kerak.")
        return cleaned

    def save(self, commit=True):
        group = super().save(commit=False)
        if not group.day_list and "days" in self.changed_data:
            group.schedule = ""  # jadval olib tashlandi — eski matn qolmasin
        if commit:
            group.save()
        return group


class StudentForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            "group",
            "full_name",
            "phone",
            "telegram",
            "status",
            "joined_at",
            "notes",
        ]
        widgets = {
            "joined_at": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "phone": forms.TextInput(attrs={"type": "tel", "placeholder": "+998 90 123 45 67"}),
            "telegram": forms.TextInput(attrs={"placeholder": "username"}),
            "notes": forms.Textarea(),
        }

    def clean_full_name(self):
        return " ".join(self.cleaned_data["full_name"].split())

    def clean_phone(self):
        phone = self.cleaned_data["phone"].strip()
        digits = [c for c in phone if c.isdigit()]
        if phone and not 7 <= len(digits) <= 15:
            raise forms.ValidationError("Telefon raqami noto‘g‘ri.")
        return phone


class ModuleForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Module
        fields = ["title", "order", "description"]
        widgets = {"description": forms.Textarea()}


class TopicForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Topic
        fields = [
            "module",
            "title",
            "description",
            "homework",
            "resources",
            "duration_minutes",
            "order",
            "is_active",
        ]
        widgets = {
            "description": forms.Textarea(),
            "homework": forms.Textarea(attrs={"rows": 3}),
            "resources": forms.Textarea(
                attrs={"rows": 3, "placeholder": "https://docs.python.org/3/tutorial/"}
            ),
        }

    def clean(self):
        cleaned = super().clean()
        title, module = cleaned.get("title"), cleaned.get("module")
        if title:
            clash = Topic.objects.filter(module=module, title__iexact=title.strip())
            if self.instance.pk:
                clash = clash.exclude(pk=self.instance.pk)
            if clash.exists():
                self.add_error("title", "Bu bo‘limda shunday mavzu allaqachon bor.")
        return cleaned


class LessonForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Lesson
        fields = [
            "group",
            "topic",
            "held_on",
            "starts_at",
            "status",
            "homework",
            "notes",
        ]
        widgets = {
            "held_on": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "starts_at": forms.TimeInput(attrs={"type": "time"}, format="%H:%M"),
            "homework": forms.Textarea(),
            "notes": forms.Textarea(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        topics = Topic.objects.filter(is_active=True).select_related("module")
        if self.instance.topic_id:
            # Yashirilgan mavzu eski darsda ham tanlangan bo'lib qolishi kerak.
            topics = Topic.objects.filter(pk=self.instance.topic_id) | topics
        self.fields["topic"].queryset = topics
        self.fields["topic"].required = False
        self.fields["group"].queryset = Group.objects.exclude(
            Q(status=Group.Status.ARCHIVED) & ~Q(pk=self.instance.group_id)
        )

    def clean(self):
        cleaned = super().clean()
        group, held_on = cleaned.get("group"), cleaned.get("held_on")
        if group and held_on and cleaned.get("status") != Lesson.Status.CANCELLED:
            clash = Lesson.objects.filter(
                group=group, held_on=held_on, starts_at=cleaned.get("starts_at")
            ).exclude(status=Lesson.Status.CANCELLED)
            if self.instance.pk:
                clash = clash.exclude(pk=self.instance.pk)
            if clash.exists():
                self.add_error(
                    "held_on", "Bu guruhda shu kun va vaqtda dars allaqachon yozilgan."
                )
        return cleaned

    def save(self, commit=True):
        lesson = super().save(commit=False)
        if not lesson.homework and lesson.topic and lesson.topic.homework:
            lesson.homework = lesson.topic.homework
        if commit:
            lesson.save()
        return lesson


class TopicImportForm(StyledFormMixin, forms.Form):
    text = forms.CharField(
        label="Mavzular matni",
        widget=forms.Textarea(attrs={"rows": 16, "spellcheck": "false"}),
    )
    groups = forms.ModelMultipleChoiceField(
        label="Guruh dasturiga ham qo‘shish",
        queryset=Group.objects.filter(status=Group.Status.ACTIVE),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    default_duration = forms.IntegerField(
        label="Standart davomiylik (daq.)", min_value=10, max_value=600, initial=90
    )

    def clean_text(self):
        parsed = parse_topics(self.cleaned_data["text"])
        if not any(m.topics for m in parsed):
            raise forms.ValidationError("Matndan birorta ham mavzu topilmadi.")
        self.parsed = parsed
        return self.cleaned_data["text"]


class QuizForm(StyledFormMixin, forms.ModelForm):
    text = forms.CharField(
        label="Savollar",
        widget=forms.Textarea(attrs={"rows": 18, "spellcheck": "false"}),
        help_text="“?” — savol, “+” — to‘g‘ri javob, “-” — noto‘g‘ri javob. "
        "Savollar orasida bo‘sh qator qoldirish mumkin.",
    )

    class Meta:
        model = Quiz
        fields = ["time_limit_minutes", "text"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["text"].widget.attrs["placeholder"] = QUIZ_FORMAT_HELP
        if self.instance.pk:
            self.fields["text"].initial = self.instance.as_text()

    def clean_text(self):
        parsed, errors = parse_quiz(self.cleaned_data["text"])
        if errors:
            raise forms.ValidationError(errors)
        if not parsed:
            raise forms.ValidationError("Kamida bitta savol yozing.")
        self.parsed = parsed
        return self.cleaned_data["text"]

    def save(self, commit=True):
        quiz = super().save(commit=commit)
        if commit:
            quiz.replace_questions(self.parsed)
        return quiz
