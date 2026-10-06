from datetime import time, timedelta
from io import StringIO

from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from academy.forms import GroupForm
from academy.models import Attendance, Group, Lesson
from academy.services import (
    attendance_trend,
    dashboard_payload,
    sessions_between,
    start_session,
    week_start,
    week_timetable,
)

from . import factories as f

EVERY_DAY = "0,1,2,3,4,5,6"


def daily_group(**kw):
    kw.setdefault("days", EVERY_DAY)
    kw.setdefault("starts_at", time(9))
    kw.setdefault("ends_at", time(10))
    return f.group(**kw)


class GroupTimetableTests(TestCase):
    def test_schedule_text_is_derived_from_days_and_times(self):
        g = f.group(days="4,1", starts_at=time(14), ends_at=time(15))
        self.assertEqual(g.day_list, [1, 4])
        self.assertEqual(g.schedule, "Se / Ju 14:00–15:00")
        self.assertTrue(g.has_timetable)

    def test_group_without_days_keeps_free_text_schedule(self):
        g = f.group(schedule="Kelishilgan holda")
        self.assertFalse(g.has_timetable)
        self.assertEqual(g.schedule, "Kelishilgan holda")

    def test_form_validates_times(self):
        base = {"name": "X", "code": "X-1", "status": "active"}
        form = GroupForm({**base, "days": ["1"]})
        self.assertIn("starts_at", form.errors)
        form = GroupForm({**base, "days": ["1"], "starts_at": "15:00", "ends_at": "14:00"})
        self.assertIn("ends_at", form.errors)

    def test_form_saves_days_and_clears_schedule_when_removed(self):
        form = GroupForm(
            {"name": "X", "code": "x-1", "status": "active", "days": ["5", "1", "4"],
             "starts_at": "14:00", "ends_at": "15:00"}
        )
        self.assertTrue(form.is_valid(), form.errors)
        g = form.save()
        self.assertEqual((g.days, g.schedule), ("1,4,5", "Se / Ju / Sha 14:00–15:00"))

        form = GroupForm({"name": "X", "code": "X-1", "status": "active"}, instance=g)
        self.assertTrue(form.is_valid(), form.errors)
        g = form.save()
        self.assertEqual((g.days, g.schedule), ("", ""))


class SessionTests(TestCase):
    def setUp(self):
        self.group = daily_group()
        self.topics = [f.topic(title=f"T{i}") for i in range(1, 4)]
        self.group.add_topics(self.topics)
        self.today = timezone.localdate()

    def test_future_sessions_get_next_topics_in_order(self):
        sessions = sessions_between(self.today, self.today + timedelta(days=3))
        self.assertEqual([s.topic for s in sessions[:3]], self.topics)
        self.assertIsNone(sessions[3].topic)  # dastur tugadi

    def test_existing_lesson_reserves_its_topic(self):
        f.lesson(self.group, topic=self.topics[0])
        today, tomorrow = sessions_between(self.today, self.today + timedelta(days=1))
        self.assertIsNotNone(today.lesson)
        self.assertEqual(today.topic, self.topics[0])
        self.assertEqual(tomorrow.topic, self.topics[1])

    def test_future_range_continues_queue_from_today(self):
        later = sessions_between(self.today + timedelta(days=1), self.today + timedelta(days=1))
        self.assertEqual(later[0].topic, self.topics[1])

    def test_inactive_and_unscheduled_groups_are_skipped(self):
        daily_group(status=Group.Status.ARCHIVED)
        f.group()
        self.assertEqual(len(sessions_between(self.today, self.today)), 1)

    def test_start_session_creates_lesson_once(self):
        lesson, created = start_session(self.group)
        self.assertTrue(created)
        self.assertEqual((lesson.topic, lesson.starts_at), (self.topics[0], time(9)))
        again, created = start_session(self.group)
        self.assertFalse(created)
        self.assertEqual(again, lesson)

    def test_week_timetable_positions_events(self):
        tt = week_timetable(week_start(self.today))
        self.assertEqual(len(tt["days"]), 7)
        item = next(d for d in tt["days"] if d["is_today"])["items"][0]
        self.assertGreater(item["height"], 0)
        self.assertGreaterEqual(item["top"], 0)

    def test_dashboard_lists_today_sessions(self):
        payload = dashboard_payload()
        self.assertEqual(len(payload["today_sessions"]), 1)
        self.assertTrue(payload["has_timetable"])


class TimetableViewTests(TestCase):
    def setUp(self):
        self.client.force_login(f.user())
        self.group = daily_group(code="TT-1")
        self.topic = f.topic(title="Sikllar")
        self.group.add_topics([self.topic])

    def test_timetable_page(self):
        for query in ("", "?hafta=2026-01-05", "?hafta=xato"):
            with self.subTest(query=query):
                self.assertContains(self.client.get(reverse("timetable") + query), "TT-1")

    def test_start_lesson_redirects_to_attendance(self):
        response = self.client.post(reverse("start_lesson", args=[self.group.pk]))
        lesson = Lesson.objects.get(group=self.group)
        self.assertRedirects(response, reverse("attendance", args=[lesson.pk]))
        self.assertEqual(lesson.topic, self.topic)
        self.client.post(reverse("start_lesson", args=[self.group.pk]))
        self.assertEqual(Lesson.objects.filter(group=self.group).count(), 1)

    def test_start_lesson_requires_post(self):
        self.assertEqual(self.client.get(reverse("start_lesson", args=[self.group.pk])).status_code, 405)

    def test_search_json_for_command_palette(self):
        f.student(self.group, full_name="Karimov Laziz")
        data = self.client.get(reverse("search"), {"q": "Laziz", "format": "json"}).json()
        self.assertEqual(data["results"][0]["kind"], "student")
        self.assertEqual(data["results"][0]["title"], "Karimov Laziz")

    def test_lesson_create_prefills_date_and_time(self):
        response = self.client.get(
            reverse("lesson_create"), {"group": self.group.pk, "sana": "2026-11-03"}
        )
        initial = response.context["form"].initial
        self.assertEqual(str(initial["held_on"]), "2026-11-03")
        self.assertEqual(initial["starts_at"], time(9))


class TrendTests(TestCase):
    def test_attendance_trend_current_week(self):
        lesson = f.lesson()
        for status in (Attendance.Status.PRESENT, Attendance.Status.ABSENT):
            Attendance.objects.create(lesson=lesson, student=f.student(lesson.group), status=status)
        trend = attendance_trend()
        self.assertEqual(len(trend), 8)
        self.assertEqual(trend[-1]["percent"], 50)
        self.assertIsNone(trend[0]["percent"])


class LoadSchoolTimetableTests(TestCase):
    def test_school_groups_get_structured_timetable(self):
        call_command("load_school", stdout=StringIO())
        g = Group.objects.get(code="S-009")
        self.assertEqual((g.days, g.starts_at, g.ends_at), ("1,4,5", time(14), time(15)))
        self.assertEqual(g.schedule, "Se / Ju / Sha 14:00–15:00")
        self.assertEqual(Group.objects.get(code="P-006").starts_at, time(16))
