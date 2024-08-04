from django.apps import AppConfig


class AppOtimaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_dashboard'

    def ready(self):
        import app_dashboard.signals