import re
from datetime import timedelta

from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import AuthenticationForm
from django.core.validators import MaxValueValidator, validate_email
from django.db.models import Count, Q
from django.utils import timezone
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _

from .models import (
    WEEKDAY_CHOICES,
    Group,
    Lesson,
    Module,
    OpenQuiz,
    Quiz,
    QuizBatch,
    QuizLanguage,
    RegistrationLink,
    Reward,
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
            {"class": "input", "placeholder": _("Login"), "autofocus": True, "autocomplete": "username"}
        )
        self.fields["password"].widget.attrs.update(
            {"class": "input", "placeholder": _("Parol"), "autocomplete": "current-password"}
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
        label=_("Dars kunlari"),
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
            "email": forms.EmailInput(attrs={"placeholder": _("ali@gmail.com"), "autocapitalize": "off"}),
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
            raise forms.ValidationError(_("Telefon raqami noto‘g‘ri."))
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
            "study_ru",
            "slides",
            "duration_minutes",
            "order",
            "is_active",
        ]
        widgets = {
            "description": forms.Textarea(),
            "homework": forms.Textarea(attrs={"rows": 3}),
            "study": forms.Textarea(attrs={"rows": 18, "spellcheck": "false"}),
            "study_ru": forms.Textarea(attrs={"rows": 18, "spellcheck": "false"}),
            "slides": forms.Textarea(attrs={"rows": 18, "spellcheck": "false"}),
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
        label=_("Mavzular matni"),
        widget=forms.Textarea(attrs={"rows": 16, "spellcheck": "false"}),
    )
    groups = forms.ModelMultipleChoiceField(
        label=_("Guruh dasturiga ham qo‘shish"),
        queryset=Group.objects.filter(status=Group.Status.ACTIVE),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    default_duration = forms.IntegerField(
        label=_("Standart davomiylik (daq.)"), min_value=10, max_value=600, initial=90
    )

    def clean_text(self):
        parsed = parse_topics(self.cleaned_data["text"])
        if not any(m.topics for m in parsed):
            raise forms.ValidationError(_("Matndan birorta ham mavzu topilmadi."))
        self.parsed = parsed
        return self.cleaned_data["text"]


class QuizForm(StyledFormMixin, forms.ModelForm):
    text = forms.CharField(
        label=_("Savollar"),
        widget=forms.Textarea(attrs={"rows": 18, "spellcheck": "false"}),
        help_text=_(
            "“?” — savol, “+” — to‘g‘ri javob, “-” — noto‘g‘ri javob. Savollar orasida bo‘sh qator qoldirish mumkin."
        ),
    )
    text_ru = forms.CharField(
        label=_("Ruscha tarjima (ixtiyoriy)"),
        required=False,
        widget=forms.Textarea(attrs={"rows": 18, "spellcheck": "false"}),
        help_text=_(
            "Xuddi o‘sha savollar xuddi o‘sha tartibda, to‘g‘ri javob (“+”) xuddi o‘sha o‘rinda. "
            "Tarjima qilinmagan savolni o‘zbekcha qoldiring. Bo‘sh — testni faqat o‘zbekcha yechish mumkin."
        ),
    )

    class Meta:
        model = Quiz
        fields = ["time_limit_minutes", "bonus_quvvat", "text", "text_ru"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["text"].widget.attrs["placeholder"] = QUIZ_FORMAT_HELP
        self.fields["text_ru"].widget.attrs["placeholder"] = (
            "? Какой скобкой записывается список в Python?\n+ [ ]\n- ( )\n- { }"
        )
        if self.instance.pk:
            self.fields["text"].initial = self.instance.as_text()
            self.fields["text_ru"].initial = self.instance.as_text_ru()
        # Yuborilmasa — testdagi joriy qiymat qoladi.
        self.fields["bonus_quvvat"].required = False

    def clean_bonus_quvvat(self):
        return self.cleaned_data.get("bonus_quvvat") or self.instance.bonus_quvvat

    def clean_text(self):
        parsed, errors = parse_quiz(self.cleaned_data["text"])
        if errors:
            raise forms.ValidationError(errors)
        if not parsed:
            raise forms.ValidationError(_("Kamida bitta savol yozing."))
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


CHANNEL_CHOICES = [("telegram", _("Telegram")), ("email", _("Email (Gmail)"))]


class QuizSendForm(StyledFormMixin, forms.Form):
    """Test jo'natish: kimga, nechta savol va qancha vaqt."""

    students = forms.ModelMultipleChoiceField(
        label=_("Shogirdlar"),
        queryset=Student.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        error_messages={"required": _("Kamida bitta shogirdni tanlang.")},
    )
    question_count = forms.IntegerField(label=_("Savollar soni"), min_value=1)
    time_limit_minutes = forms.IntegerField(
        label=_("Vaqt (daqiqa)"), min_value=1, max_value=QuizBatch.MAX_TIME_LIMIT
    )
    scheduled_at = forms.DateTimeField(
        label=_("Qachon yuborilsin?"),
        required=False,
        input_formats=["%Y-%m-%dT%H:%M"],
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"),
        help_text=_("Bo‘sh — darhol. Vaqt ko‘rsatilsa, havolalar o‘sha paytda avtomatik yuboriladi."),
    )
    channels = forms.MultipleChoiceField(
        label=_("Qayerga yuborilsin?"),
        choices=CHANNEL_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        help_text=_("Hech biri tanlanmasa — havolalar faqat yaratiladi, o‘zingiz tarqatasiz."),
    )

    SCHEDULE_MAX_DAYS = 30

    def clean_scheduled_at(self):
        value = self.cleaned_data["scheduled_at"]
        now = timezone.now()
        if value and value <= now + timedelta(minutes=1):
            raise forms.ValidationError(_("Kelajakdagi vaqtni tanlang (yoki bo‘sh qoldiring — darhol)."))
        if value and value > now + timedelta(days=self.SCHEDULE_MAX_DAYS):
            raise forms.ValidationError(
                _("Ko‘pi bilan {SCHEDULE_MAX_DAYS} kun oldinga.").format(SCHEDULE_MAX_DAYS=self.SCHEDULE_MAX_DAYS)
            )
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
        label=_("Ro‘yxat"),
        widget=forms.Textarea(attrs={"rows": 14, "spellcheck": "false"}),
    )
    group = forms.ModelChoiceField(
        label=_("Guruh"),
        queryset=Group.objects.order_by("name"),
        required=False,
        empty_label=_("Barcha guruhlar"),
        help_text=_("Bir xil ismli o‘quvchilar boshqa guruhda bo‘lsa, guruhni tanlang."),
    )


class ContactSelfForm(forms.Form):
    """O'quvchining o'zi to'ldiradigan ochiq forma (guruh havolasi orqali)."""

    student = forms.ModelChoiceField(
        label=_("Ismingiz"), queryset=Student.objects.none(), empty_label=_("— ismingizni tanlang —")
    )
    telegram = forms.CharField(label=_("Telegram username"), max_length=80, required=False)
    phone = forms.CharField(label=_("Telefon raqami"), max_length=40, required=False)
    email = forms.EmailField(label=_("Email"), required=False)

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
                _("Username noto‘g‘ri: 5–32 ta lotin harf, raqam yoki “_” (masalan, @ali_2010).")
            )
        return value

    def clean_phone(self):
        raw = self.cleaned_data["phone"].strip()
        value = normalize_phone(raw)
        if raw and not value:
            raise forms.ValidationError(_("Telefon raqami noto‘g‘ri (masalan, +998 90 123 45 67)."))
        return value

    def clean(self):
        data = super().clean()
        if data.get("email"):
            data["email"] = data["email"].strip().lower()
        if not self.errors and not (data.get("telegram") or data.get("phone") or data.get("email")):
            raise forms.ValidationError(_("Telegram username, telefon yoki emailni kiriting."))
        return data


class RegistrationForm(forms.Form):
    """Ochiq ro'yxatdan o'tish formasi (o'quvchi to'ldiradi)."""

    full_name = forms.CharField(label=_("Familiya, ism, otasining ismi"), max_length=160)
    phone = forms.CharField(label=_("Telefon raqami"), max_length=40)
    telegram = forms.CharField(label=_("Telegram username"), max_length=80)
    email = forms.EmailField(label=_("Email (ixtiyoriy)"), required=False)

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("label_suffix", "")
        super().__init__(*args, **kwargs)
        attrs = {
            "full_name": {"placeholder": _("Aliyev Sardor Akmalovich"), "autocomplete": "name"},
            "phone": {"placeholder": "+998 90 123 45 67", "inputmode": "tel", "autocomplete": "tel"},
            "telegram": {"placeholder": _("@username"), "autocomplete": "off", "autocapitalize": "off"},
            "email": {"placeholder": _("ali@gmail.com"), "autocomplete": "email", "autocapitalize": "off"},
        }
        for name, field in self.fields.items():
            field.widget.attrs.update(attrs[name], **{"class": "input"})

    def clean_full_name(self):
        name = " ".join(self.cleaned_data["full_name"].split())
        if len(name.split()) < 2:
            raise forms.ValidationError(_("Familiya va ismingizni to‘liq yozing."))
        # Hammasi kichik yoki katta harfda yozilgan bo'lsa — "Aliyev Sardor" ko'rinishiga.
        return name.title() if name.islower() or name.isupper() else name

    def clean_phone(self):
        value = normalize_phone(self.cleaned_data["phone"])
        if not value:
            raise forms.ValidationError(_("Telefon raqami noto‘g‘ri (masalan, +998 90 123 45 67)."))
        return value

    def clean_telegram(self):
        value = normalize_username(self.cleaned_data["telegram"])
        if not value:
            raise forms.ValidationError(
                _("Username noto‘g‘ri: 5–32 ta lotin harf, raqam yoki “_” (masalan, @ali_2010).")
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


class RewardForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Reward
        fields = ["title", "cost", "perk", "description", "order", "is_active"]


# --- Umumiy test havolasi -------------------------------------------------------

EMAIL_SPLIT = re.compile(r"[\s,;]+")
MAX_INVITES = 200


def parse_emails(text: str) -> tuple[list[str], list[str]]:
    """Matndan email manzillar (vergul, nuqtali vergul, bo'sh joy yoki yangi qator bilan).
    Qaytaradi: (to'g'rilari — takrorlarsiz, kichik harfda; noto'g'rilari)."""
    good, bad, seen = [], [], set()
    for raw in EMAIL_SPLIT.split(text or ""):
        value = raw.strip().strip("<>()\"'").lower()
        if not value:
            continue
        try:
            validate_email(value)
        except forms.ValidationError:
            bad.append(raw.strip())
            continue
        if value not in seen:
            seen.add(value)
            good.append(value)
    return good, bad


class EmailListField(forms.CharField):
    """Bir nechta email manzil: ro'yxat qaytaradi, noto'g'rilarini aniq ko'rsatadi."""

    widget = forms.Textarea

    def to_python(self, value):
        return parse_emails(super().to_python(value))

    def validate(self, value):
        good, bad = value
        if bad:
            shown = ", ".join(bad[:5]) + ("…" if len(bad) > 5 else "")
            raise forms.ValidationError(_("Noto‘g‘ri email: {emails}").format(emails=shown))
        if self.required and not good:
            raise forms.ValidationError(_("Kamida bitta email manzil kiriting."))
        if len(good) > MAX_INVITES:
            raise forms.ValidationError(_("Bir martada ko‘pi bilan {n} ta manzil.").format(n=MAX_INVITES))

    def run_validators(self, value):
        super().run_validators(" ".join(value[0]))

    def clean(self, value):
        return super().clean(value)[0]


EMAILS_HELP = _(
    "Vergul bilan yoki har birini yangi qatordan yozing. Har biriga alohida xat boradi — "
    "manzillar bir-biriga ko‘rinmaydi."
)


class OpenQuizForm(StyledFormMixin, forms.ModelForm):
    """Umumiy havola yaratish: test, savollar soni, vaqt, til va (ixtiyoriy) emailga yuborish."""

    emails = EmailListField(
        label=_("Emailga yuborish"),
        required=False,
        help_text=EMAILS_HELP,
        widget=forms.Textarea(attrs={"rows": 4, "placeholder": "ali@gmail.com, vali@mail.ru"}),
    )

    class Meta:
        model = OpenQuiz
        fields = ["quiz", "title", "language", "question_count", "time_limit_minutes", "closes_at"]
        widgets = {
            "closes_at": forms.DateTimeInput(attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        quizzes = (
            Quiz.objects.filter(questions__isnull=False)
            .select_related("topic__module")
            .annotate(n=Count("questions", distinct=True))
            .order_by("topic__module__order", "topic__order", "topic__title")
        )
        self.bank = {q.pk: q.n for q in quizzes}
        field = self.fields["quiz"]
        field.queryset = quizzes
        field.label = _("Mavzu testi")
        field.label_from_instance = lambda q: _("{topic} · {n} ta savol").format(
            topic=q.topic.title_in(get_language()), n=q.n
        )
        self.fields["closes_at"].input_formats = ["%Y-%m-%dT%H:%M"]
        if not self.is_bound and not self.instance.pk:
            self.initial.setdefault("question_count", 10)
            self.initial.setdefault("time_limit_minutes", 10)

    def clean_closes_at(self):
        value = self.cleaned_data["closes_at"]
        if value and value <= timezone.now():
            raise forms.ValidationError(_("Kelajakdagi vaqtni tanlang (yoki bo‘sh qoldiring)."))
        return value

    def clean(self):
        data = super().clean()
        quiz, count = data.get("quiz"), data.get("question_count")
        if quiz and count and count > self.bank.get(quiz.pk, 0):
            self.add_error(
                "question_count",
                _("Bu testda {n} ta savol bor — ko‘pi bilan shuncha.").format(n=self.bank.get(quiz.pk, 0)),
            )
        return data


class OpenQuizInviteForm(StyledFormMixin, forms.Form):
    emails = EmailListField(
        label=_("Email manzillar"),
        help_text=EMAILS_HELP,
        widget=forms.Textarea(attrs={"rows": 4, "placeholder": "ali@gmail.com, vali@mail.ru"}),
    )


class TeacherForm(StyledFormMixin, forms.Form):
    """Bosh ustoz: o'qituvchi logini, paroli va guruhlari."""

    first_name = forms.CharField(label=_("Ism"), max_length=150)
    last_name = forms.CharField(label=_("Familiya"), max_length=150, required=False)
    username = forms.RegexField(
        label=_("Login"),
        regex=r"^[A-Za-z0-9_.-]{3,40}$",
        error_messages={"invalid": _("Login: 3–40 ta lotin harfi, raqam yoki _ . - belgisi.")},
    )
    password = forms.CharField(
        label=_("Parol"),
        required=False,
        widget=forms.PasswordInput(render_value=False, attrs={"autocomplete": "new-password"}),
        help_text=_("Kamida 8 belgi. Tahrirlashda bo‘sh qoldirilsa — eski parol qoladi."),
    )
    groups = forms.ModelMultipleChoiceField(
        label=_("Guruhlari"),
        queryset=Group.objects.none(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        help_text=_("O‘qituvchi faqat shu guruhlarni ko‘radi va ularga test yuboradi."),
    )
    permissions = forms.MultipleChoiceField(
        label=_("Nimalarga ruxsat"),
        choices=(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        help_text=_(
            "O‘qituvchi panelida qaysi bo‘limlar ko‘rinadi. Har bir bo‘limda u faqat o‘z guruhlarining "
            "ma’lumotini ko‘radi. “Mening guruhlarim” va “Test jo‘natish” doim ochiq."
        ),
    )
    is_active = forms.BooleanField(label=_("Faol (tizimga kira oladi)"), required=False, initial=True)

    def __init__(self, *args, user=None, **kwargs):
        from .teachers import SECTIONS

        self.user = user
        if user is not None:
            account = getattr(user, "teacher_account", None)
            kwargs.setdefault(
                "initial",
                {
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "username": user.username,
                    "groups": list(Group.objects.filter(teacher=user)),
                    "permissions": list(account.permissions) if account else [],
                    "is_active": user.is_active,
                },
            )
        super().__init__(*args, **kwargs)
        self.fields["permissions"].choices = [(key, label) for key, label, _pages in SECTIONS]
        self.fields["groups"].queryset = Group.objects.exclude(status=Group.Status.ARCHIVED).order_by("name")
        if user is None:
            self.fields["password"].required = True
            del self.fields["is_active"]

    def clean_username(self):
        username = self.cleaned_data["username"]
        clash = get_user_model().objects.filter(username__iexact=username)
        if self.user is not None:
            clash = clash.exclude(pk=self.user.pk)
        if clash.exists():
            raise forms.ValidationError(_("Bu login band — boshqasini tanlang."))
        return username

    def clean_password(self):
        password = self.cleaned_data["password"]
        if password:
            password_validation.validate_password(password, self.user)
        return password
