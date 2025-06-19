from django.apps import AppConfig

class BeamConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'beam'  # Просто имя приложения

    def ready(self):
        """Активация сигналов при запуске приложения"""
        # Импорт модуля signals активирует все @receiver декораторы
        from . import signals