from django.apps import AppConfig


class ModuletrackConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ModuleTrack'

    def ready(self):
        import ModuleTrack.signals
