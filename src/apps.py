from django.apps import AppConfig


class AppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "src"
    verbose_name = "Quản lý hóa đơn"

    def ready(self):
        import src.signals  # noqa: F401, PLC0415
