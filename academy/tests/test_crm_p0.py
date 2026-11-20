"""CRM redizayn P0: bosh sahifa ustuvorligi, halol KPI, jadval yo'laklari va agenda, guruh, yo'qlama, menyu."""

from datetime import time
from types import SimpleNamespace

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from academy import teachers
from academy.models import Attendance, Lesson, SyllabusItem
from academy.services import dashboard_payload, next_up_session, place_in_lanes
from academy.views import syllabus_by_module

from . import factories as f


class DashboardHonestKpiTests(TestCase):
    def test_no_marked_attendance_is_none_not_zero(self):
        f.student(f.group())
        stats = dashboard_payload()["stats"]
        self.assertIsNone(stats["attendance_pct"])
        self.assertEqual(stats["attendance_marked"], 0)
        self.assertIsNone(stats["syllabus_pct"])  # dastur biriktirilmagan

    def test_real_zero_attendance_is_zero_with_denominator(self):
        g = f.group()
        s = f.student(g)
        lesson = f.lesson(g, days=-1, status=Lesson.Status.COMPLETED)
        Attendance.objects.create(lesson=lesson, student=s, status=Attendance.Status.ABSENT)
        stats = dashboard_payload()["stats"]
        self.assertEqual((stats["attendance_pct"], stats["attendance_present"], stats["attendance_marked"]), (0, 0, 1))

    def test_overdue_count_is_full_count_not_truncated_list(self):
        g = f.group()
        for d in range(2, 11):
            f.lesson(g, days=-d)
        payload = dashboard_payload()
        self.assertEqual(payload["overdue_count"], 9)
        self.assertEqual(len(payload["overdue"]), 6)

    def test_page_shows_no_data_and_next_lesson_block(self):
        self.client.force_login(f.user())
        page = self.client.get(reverse("dashboard"))
        self.assertContains(page, "data-next-lesson")
        self.assertContains(page, "Ma’lumot yo‘q")
        self.assertNotContains(page, "<div class=\"kpi-value tabular\">0<small>%</small>")


class NextUpPriorityTests(TestCase):
    def test_live_then_upcoming_then_missed_then_later(self):
        live, up, missed, later = (SimpleNamespace(state=s) for s in ("live", "upcoming", "missed", "upcoming"))
        self.assertIs(next_up_session([missed, up, live], [later]), live)
        self.assertIs(next_up_session([missed, up], [later]), up)
        self.assertIs(next_up_session([missed], [later]), missed)
        self.assertIs(next_up_session([SimpleNamespace(state="done")], [later]), later)
        self.assertIsNone(next_up_session([], []))


class TimetableLanesAndAgendaTests(TestCase):
    def test_concurrent_blocks_get_separate_lanes(self):
        items = place_in_lanes([{"top": 10, "height": 20}, {"top": 10, "height": 20}, {"top": 50, "height": 10}])
        self.assertEqual([(i["lane"], i["lanes"]) for i in items], [(0, 2), (1, 2), (0, 1)])

    def test_agenda_selects_requested_day_and_falls_back(self):
        self.client.force_login(f.user())
        today = timezone.localdate()
        g = f.group(days=str(today.weekday()), starts_at=time(9), ends_at=time(10))
        ctx = self.client.get(reverse("timetable")).context
        self.assertEqual(ctx["selected_day"], today)
        self.assertEqual([s.group for s in ctx["selected_sessions"]], [g])
        other = ctx["days"][(today.weekday() + 1) % 7]["date"]
        ctx = self.client.get(reverse("timetable"), {"hafta": today.isoformat(), "kun": other.isoformat()}).context
        self.assertEqual((ctx["selected_day"], ctx["selected_sessions"]), (other, []))
        ctx = self.client.get(reverse("timetable"), {"kun": "2000-01-01"}).context  # boshqa hafta — bugun
        self.assertEqual(ctx["selected_day"], today)


class GroupDetailSectionsTests(TestCase):
    def test_only_module_with_next_topic_is_open_and_deep_links_kept(self):
        self.client.force_login(f.user())
        g = f.group()
        m1, m2 = f.module(title="Kirish"), f.module(title="Sikllar")
        t1, t2, t3 = f.topic(module=m1), f.topic(module=m2), f.topic(module=m2)
        a = SyllabusItem.objects.create(group=g, topic=t1, order=1, status=SyllabusItem.Status.TAUGHT)
        SyllabusItem.objects.create(group=g, topic=t2, order=2)
        SyllabusItem.objects.create(group=g, topic=t3, order=3)
        sections = syllabus_by_module(list(g.syllabus.select_related("topic", "topic__module")), g.next_syllabus_item())
        self.assertEqual([(s["module"].title, s["open"], s["taught"]) for s in sections],
                         [("Kirish", False, 1), ("Sikllar", True, 0)])
        page = self.client.get(g.get_absolute_url())
        anchors = ('href="#shogirdlar"', 'href="#dastur"', 'id="shogirdlar"', 'id="dastur"', f'id="syllabus-{a.pk}"')
        for anchor in anchors:
            self.assertContains(page, anchor)


class AttendanceSheetTests(TestCase):
    def test_save_semantics_unchanged_and_unsaved_rows_flagged(self):
        self.client.force_login(f.user())
        g = f.group()
        s1, s2 = f.student(g), f.student(g)
        lesson = f.lesson(g)
        Attendance.objects.create(lesson=lesson, student=s1, status=Attendance.Status.LATE)
        page = self.client.get(reverse("attendance", args=[lesson.pk]))
        self.assertContains(page, 'data-saved="1"', count=1)
        self.assertContains(page, 'data-saved="0"', count=1)
        self.assertContains(page, 'name="complete" value="1"')
        self.assertContains(page, 'name="then" value="quiz"')
        # Asosiy amal hamon saqlaydi va darsni yakunlaydi.
        data = {f"status_{s1.pk}": "present", f"status_{s2.pk}": "absent", "complete": "1"}
        self.client.post(reverse("attendance", args=[lesson.pk]), data)
        lesson.refresh_from_db()
        self.assertEqual(lesson.status, Lesson.Status.COMPLETED)
        self.assertEqual(Attendance.objects.get(lesson=lesson, student=s2).status, Attendance.Status.ABSENT)


class NavigationTests(TestCase):
    def test_badges_only_for_work_and_queues_grouped(self):
        self.client.force_login(f.user())
        page = self.client.get(reverse("dashboard"))
        self.assertContains(page, "Navbatlar")
        self.assertNotIn("nav_students", page.context)

    def test_teacher_without_queue_permissions_sees_no_queue_group(self):
        teacher = f.user(username="ustoz2")
        g = f.group(teacher=teacher)
        account = teachers.account_of(teacher)
        account.telegram_id, account.linked_at = 777, timezone.now()
        account.permissions = ["groups"]
        account.save()
        self.client.force_login(teacher)
        page = self.client.get(g.get_absolute_url())
        self.assertEqual(page.status_code, 200)
        self.assertNotContains(page, ">Navbatlar<")
        self.assertNotContains(page, reverse("registrations"))
