from datetime import timedelta

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.validators import MaxValueValidator
from django.db.models import Q
from django.utils import timezone

from .models import (
    WEEKDAY_CHOICES,
    Group,
    Lesson,
    Module,
    Quiz,
    QuizBatch,
    QuizLanguage,
    RegistrationLink,
    Student,
    Topic,
)
from .quiz_format import translation_errors
from .services import QUIZ_FORMAT_HELP, parse_quiz, parse_topics
from .telegram_sender import normalize_phone, normalize_username


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
            "telegram_chat",
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
            "email",
            "quiz_language",
            "status",
            "joined_at",
            "notes",
        ]
        widgets = {
            "joined_at": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "phone": forms.TextInput(attrs={"type": "tel", "placeholder": "+998 90 123 45 67"}),
            "telegram": forms.TextInput(attrs={"placeholder": "username"}),
            "email": forms.EmailInput(attrs={"placeholder": "ali@gmail.com", "autocapitalize": "off"}),
            "notes": forms.Textarea(),
        }

    def clean_full_name(self):
        return " ".join(self.cleaned_data["full_name"].split())

    def clean_email(self):
        return self.cleaned_data["email"].strip().lower()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Eski formalar/importlar bu maydonni yubormasa — o'zbekcha.
        self.fields["quiz_language"].required = False

    def clean_quiz_language(self):
        return self.cleaned_data["quiz_language"] or QuizLanguage.UZ

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
            "title_ru",
            "description",
            "homework",
            "resources",
            "study",
            "duration_minutes",
            "order",
            "is_active",
        ]
        widgets = {
            "description": forms.Textarea(),
            "homework": forms.Textarea(attrs={"rows": 3}),
            "study": forms.Textarea(attrs={"rows": 18, "spellcheck": "false"}),
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
    text_ru = forms.CharField(
        label="Ruscha tarjima (ixtiyoriy)",
        required=False,
        widget=forms.Textarea(attrs={"rows": 18, "spellcheck": "false"}),
        help_text="Xuddi o‘sha savollar xuddi o‘sha tartibda, to‘g‘ri javob (“+”) xuddi o‘sha "
        "o‘rinda. Tarjima qilinmagan savolni o‘zbekcha qoldiring. Bo‘sh — testni faqat "
        "o‘zbekcha yechish mumkin.",
    )

    class Meta:
        model = Quiz
        fields = ["time_limit_minutes", "text", "text_ru"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["text"].widget.attrs["placeholder"] = QUIZ_FORMAT_HELP
        self.fields["text_ru"].widget.attrs["placeholder"] = (
            "? Какой скобкой записывается список в Python?\n+ [ ]\n- ( )\n- { }"
        )
        if self.instance.pk:
            self.fields["text"].initial = self.instance.as_text()
            self.fields["text_ru"].initial = self.instance.as_text_ru()

    def clean_text(self):
        parsed, errors = parse_quiz(self.cleaned_data["text"])
        if errors:
            raise forms.ValidationError(errors)
        if not parsed:
            raise forms.ValidationError("Kamida bitta savol yozing.")
        self.parsed = parsed
        return self.cleaned_data["text"]

    def clean_text_ru(self):
        text = self.cleaned_data["text_ru"]
        self.parsed_ru = []
        if not text.strip():
            return text
        parsed, errors = parse_quiz(text)
        if errors:
            raise forms.ValidationError(errors)
        self.parsed_ru = parsed
        return text

    def clean(self):
        data = super().clean()
        if getattr(self, "parsed", None) and getattr(self, "parsed_ru", None):
            errors = translation_errors(self.parsed, self.parsed_ru)
            if errors:
                self.add_error("text_ru", errors)
        return data

    def save(self, commit=True):
        quiz = super().save(commit=commit)
        if commit:
            quiz.replace_questions(self.parsed)
            self.translated = quiz.apply_translation(self.parsed_ru)
        return quiz


CHANNEL_CHOICES = [("telegram", "Telegram"), ("email", "Email (Gmail)")]


class QuizSendForm(StyledFormMixin, forms.Form):
    """Test jo'natish: kimga, nechta savol va qancha vaqt."""

    students = forms.ModelMultipleChoiceField(
        label="Shogirdlar",
        queryset=Student.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        error_messages={"required": "Kamida bitta shogirdni tanlang."},
    )
    question_count = forms.IntegerField(label="Savollar soni", min_value=1)
    time_limit_minutes = forms.IntegerField(
        label="Vaqt (daqiqa)", min_value=1, max_value=QuizBatch.MAX_TIME_LIMIT
    )
    scheduled_at = forms.DateTimeField(
        label="Qachon yuborilsin?",
        required=False,
        input_formats=["%Y-%m-%dT%H:%M"],
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"),
        help_text="Bo‘sh — darhol. Vaqt ko‘rsatilsa, havolalar o‘sha paytda avtomatik yuboriladi.",
    )
    channels = forms.MultipleChoiceField(
        label="Qayerga yuborilsin?",
        choices=CHANNEL_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        help_text="Hech biri tanlanmasa — havolalar faqat yaratiladi, o‘zingiz tarqatasiz.",
    )

    SCHEDULE_MAX_DAYS = 30

    def clean_scheduled_at(self):
        value = self.cleaned_data["scheduled_at"]
        now = timezone.now()
        if value and value <= now + timedelta(minutes=1):
            raise forms.ValidationError("Kelajakdagi vaqtni tanlang (yoki bo‘sh qoldiring — darhol).")
        if value and value > now + timedelta(days=self.SCHEDULE_MAX_DAYS):
            raise forms.ValidationError(f"Ko‘pi bilan {self.SCHEDULE_MAX_DAYS} kun oldinga.")
        return value

    def clean(self):
        data = super().clean()
        if data.get("scheduled_at") and not data.get("channels"):
            self.add_error("channels", "Rejalashtirilgan yuborish uchun kamida bitta kanalni tanlang.")
        return data

    def __init__(self, *args, quiz: Quiz, students, **kwargs):
        self.bank_size = quiz.questions.count()
        kwargs.setdefault(
            "initial",
            {
                "question_count": min(10, self.bank_size),
                "time_limit_minutes": quiz.time_limit_minutes,
                "channels": ["telegram"],
            },
        )
        super().__init__(*args, **kwargs)
        self.fields["students"].queryset = students
        count = self.fields["question_count"]
        count.max_value = self.bank_size
        count.validators.append(MaxValueValidator(self.bank_size))
        count.widget.attrs.update(min=1, max=self.bank_size, inputmode="numeric")
        self.fields["time_limit_minutes"].widget.attrs.update(inputmode="numeric")


class ContactImportForm(StyledFormMixin, forms.Form):
    """Telegram/telefonlarni ro'yxatdan ommaviy kiritish (ko'rib chiqish → tasdiqlash)."""

    text = forms.CharField(
        label="Ro‘yxat",
        widget=forms.Textarea(attrs={"rows": 14, "spellcheck": "false"}),
    )
    group = forms.ModelChoiceField(
        label="Guruh",
        queryset=Group.objects.order_by("name"),
        required=False,
        empty_label="Barcha guruhlar",
        help_text="Bir xil ismli o‘quvchilar boshqa guruhda bo‘lsa, guruhni tanlang.",
    )


class ContactSelfForm(forms.Form):
    """O'quvchining o'zi to'ldiradigan ochiq forma (guruh havolasi orqali)."""

    student = forms.ModelChoiceField(
        label="Ismingiz", queryset=Student.objects.none(), empty_label="— ismingizni tanlang —"
    )
    telegram = forms.CharField(label="Telegram username", max_length=80, required=False)
    phone = forms.CharField(label="Telefon raqami", max_length=40, required=False)
    email = forms.EmailField(label="Email", required=False)

    def __init__(self, *args, students, **kwargs):
        kwargs.setdefault("label_suffix", "")
        super().__init__(*args, **kwargs)
        self.fields["student"].queryset = students
        self.fields["telegram"].widget.attrs.update(
            placeholder="@username", autocomplete="off", autocapitalize="off"
        )
        self.fields["phone"].widget.attrs.update(
            placeholder="+998 90 123 45 67", inputmode="tel", autocomplete="tel"
        )
        self.fields["email"].widget.attrs.update(
            placeholder="ali@gmail.com", autocomplete="email", autocapitalize="off"
        )
        for f in self.fields.values():
            f.widget.attrs.setdefault("class", "input")

    def clean_telegram(self):
        raw = self.cleaned_data["telegram"].strip()
        value = normalize_username(raw)
        if raw and not value:
            raise forms.ValidationError(
                "Username noto‘g‘ri: 5–32 ta lotin harf, raqam yoki “_” (masalan, @ali_2010)."
            )
        return value

    def clean_phone(self):
        raw = self.cleaned_data["phone"].strip()
        value = normalize_phone(raw)
        if raw and not value:
            raise forms.ValidationError("Telefon raqami noto‘g‘ri (masalan, +998 90 123 45 67).")
        return value

    def clean(self):
        data = super().clean()
        if data.get("email"):
            data["email"] = data["email"].strip().lower()
        if not self.errors and not (data.get("telegram") or data.get("phone") or data.get("email")):
            raise forms.ValidationError("Telegram username, telefon yoki emailni kiriting.")
        return data


class RegistrationForm(forms.Form):
    """Ochiq ro'yxatdan o'tish formasi (o'quvchi to'ldiradi)."""

    full_name = forms.CharField(label="Familiya, ism, otasining ismi", max_length=160)
    phone = forms.CharField(label="Telefon raqami", max_length=40)
    telegram = forms.CharField(label="Telegram username", max_length=80)
    email = forms.EmailField(label="Email (ixtiyoriy)", required=False)

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("label_suffix", "")
        super().__init__(*args, **kwargs)
        attrs = {
            "full_name": {"placeholder": "Aliyev Sardor Akmalovich", "autocomplete": "name"},
            "phone": {"placeholder": "+998 90 123 45 67", "inputmode": "tel", "autocomplete": "tel"},
            "telegram": {"placeholder": "@username", "autocomplete": "off", "autocapitalize": "off"},
            "email": {"placeholder": "ali@gmail.com", "autocomplete": "email", "autocapitalize": "off"},
        }
        for name, field in self.fields.items():
            field.widget.attrs.update(attrs[name], **{"class": "input"})

    def clean_full_name(self):
        name = " ".join(self.cleaned_data["full_name"].split())
        if len(name.split()) < 2:
            raise forms.ValidationError("Familiya va ismingizni to‘liq yozing.")
        # Hammasi kichik yoki katta harfda yozilgan bo'lsa — "Aliyev Sardor" ko'rinishiga.
        return name.title() if name.islower() or name.isupper() else name

    def clean_phone(self):
        value = normalize_phone(self.cleaned_data["phone"])
        if not value:
            raise forms.ValidationError("Telefon raqami noto‘g‘ri (masalan, +998 90 123 45 67).")
        return value

    def clean_telegram(self):
        value = normalize_username(self.cleaned_data["telegram"])
        if not value:
            raise forms.ValidationError(
                "Username noto‘g‘ri: 5–32 ta lotin harf, raqam yoki “_” (masalan, @ali_2010)."
            )
        return value

    def clean_email(self):
        return self.cleaned_data["email"].strip().lower()


class RegistrationLinkForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = RegistrationLink
        fields = ["title", "group"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["group"].queryset = Group.objects.filter(status=Group.Status.ACTIVE)
        self.fields["group"].empty_label = "— guruhsiz (tasdiqlashda tanlanadi) —"
