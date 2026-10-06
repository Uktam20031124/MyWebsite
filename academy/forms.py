from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import Group, Lesson, Student, Topic


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
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            widget = field.widget
            if isinstance(widget, forms.CheckboxInput):
                widget.attrs.setdefault("class", "check")
            elif isinstance(widget, forms.Select):
                widget.attrs.setdefault("class", "input")
            elif isinstance(widget, forms.Textarea):
                widget.attrs.setdefault("class", "input")
                widget.attrs.setdefault("rows", 4)
            else:
                widget.attrs.setdefault("class", "input")
            if field.required and not widget.attrs.get("placeholder"):
                widget.attrs.setdefault("placeholder", field.label or name)


class GroupForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Group
        fields = ["name", "code", "schedule", "room", "start_date", "status", "notes"]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(),
        }


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
            "joined_at": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(),
        }


class TopicForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Topic
        fields = ["title", "description", "duration_minutes", "order", "is_active"]
        widgets = {"description": forms.Textarea()}


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
            "held_on": forms.DateInput(attrs={"type": "date"}),
            "starts_at": forms.TimeInput(attrs={"type": "time"}),
            "homework": forms.Textarea(),
            "notes": forms.Textarea(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["topic"].queryset = Topic.objects.filter(is_active=True)
        self.fields["topic"].required = False
