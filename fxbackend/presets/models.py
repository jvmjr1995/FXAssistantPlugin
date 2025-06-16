from django.db import models

# This model represents a saved FX chain preset for your plugin.
class Preset(models.Model):
    # A unique name given to each preset (e.g., "DreamyReverb").
    name = models.CharField(max_length=100, unique=True)

    # The actual plugin state or FX chain data, stored as a JSON object.
    data = models.JSONField()

    # Timestamp for when the preset was created.
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Makes the admin panel and logs show the preset's name instead of "Preset object"
        return self.name