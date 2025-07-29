from django.apps import AppConfig


class PresetsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "presets"

def ready(self):
    import presets.models # 👈 Ensures your token signal gets registered when the app loads
