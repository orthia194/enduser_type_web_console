from django.apps import AppConfig


class AdminappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'adminapp'

    def ready(self):
            import adminapp.signals  # 신호 핸들러 등록