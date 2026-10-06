from datetime import timedelta
from itertools import count

from django.contrib.auth import get_user_model
from django.utils import timezone

from academy.models import Group, Lesson, Module, Student, Topic

_seq = count(1)


def user(**kw):
    n = next(_seq)
    return get_user_model().objects.create_user(
        username=kw.pop("username", f"user{n}"), password=kw.pop("password", "pass12345!"), **kw
    )


def group(**kw):
    n = next(_seq)
    kw.setdefault("name", f"Guruh {n}")
    kw.setdefault("code", f"G-{n}")
    return Group.objects.create(**kw)


def student(group_=None, **kw):
    kw.setdefault("full_name", f"Shogird {next(_seq)}")
    return Student.objects.create(group=group_ or group(), **kw)


def module(**kw):
    kw.setdefault("title", f"Bo'lim {next(_seq)}")
    return Module.objects.create(**kw)


def topic(**kw):
    n = next(_seq)
    kw.setdefault("title", f"Mavzu {n}")
    kw.setdefault("order", n)
    return Topic.objects.create(**kw)


def lesson(group_=None, days=0, **kw):
    kw.setdefault("held_on", timezone.localdate() + timedelta(days=days))
    return Lesson.objects.create(group=group_ or group(), **kw)
