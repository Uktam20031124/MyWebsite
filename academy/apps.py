from django.apps import AppConfig


class AcademyConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "academy"
    verbose_name = "Minar Test"

    def ready(self):
        from . import audit  # noqa: F401 — kirish/chiqish signallari (harakatlar jurnali)
