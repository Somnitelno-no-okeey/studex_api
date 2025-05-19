from django.apps import AppConfig


class DisciplinesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.disciplines'

    def ready(self):
        import apps.disciplines.signals