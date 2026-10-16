from django.test import TestCase
from django.urls import reverse

from academy.models import RegistrationLink

from . import factories as f

TURBO = {"HTTP_X_TURBO_REQUEST_ID": "abc-123"}


class TurboFormStatusTests(TestCase):
    def setUp(self):
        self.client.force_login(f.user())

    def test_invalid_form_from_turbo_gets_422(self):
        response = self.client.post(reverse("group_create"), {"name": ""}, **TURBO)
        self.assertEqual(response.status_code, 422)
        self.assertContains(response, "errorlist", status_code=422)

    def test_plain_browser_and_redirects_untouched(self):
        self.assertEqual(self.client.post(reverse("group_create"), {"name": ""}).status_code, 200)
        group = f.group()
        response = self.client.post(reverse("group_contact_link", args=[group.pk]), **TURBO)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.get(reverse("group_list"), **TURBO).status_code, 200)


class TurboTemplateTests(TestCase):
    def test_app_pages_load_turbo_once_in_head(self):
        self.client.force_login(f.user())
        html = self.client.get(reverse("dashboard")).content.decode()
        head, body = html.split("</head>", 1)
        self.assertIn("vendor/turbo-8.0.12.umd.js", head)
        self.assertIn("js/app.js", head)
        # <body>dagi skriptlar Turbo har bir o'tishda qayta ishga tushiradi — app.js u yerda bo'lmasin.
        self.assertNotIn("js/app.js", body)
        self.assertIn('data-turbo-track="reload"', head)

    def test_downloads_and_logout_bypass_turbo(self):
        self.client.force_login(f.user())
        students = self.client.get(reverse("student_list")).content.decode()
        self.assertRegex(students, r'data-turbo="false" href="/shogirdlar/eksport/')
        self.assertIn('"download": true', students)
        self.assertRegex(students, r'action="/chiqish/" data-turbo="false"')
        topics = self.client.get(reverse("topic_list")).content.decode()
        self.assertRegex(topics, r'data-turbo="false" href="/mavzular/eksport/"')
        group = f.group()
        journal = self.client.get(reverse("group_journal", args=[group.pk])).content.decode()
        self.assertIn('data-turbo="false" href="/guruhlar/', journal)

    def test_public_pages_without_turbo(self):
        link = RegistrationLink.objects.create(title="S-009 chat")
        html = self.client.get(link.get_absolute_url()).content.decode()
        self.assertNotIn("turbo", html.lower().replace("data-turbo-track", ""))
