from django.db import models
from django.contrib.auth.models import User     # This is Django’s built-in user model
from django.conf import settings                # Access global settings (for AUTH_USER_MODEL)
from django.db.models.signals import post_save  # Signal triggered after saving a model
from django.dispatch import receiver            # Decorator to register a signal receiver
from rest_framework.authtoken.models import Token   # The Token model from DRF

# This model represents a saved FX chain preset for your plugin.
class Preset(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,   # Delete the preset if the user is deleted
        related_name='presets'      # Allows reverse lookup: user.presets.all()
    )
    name = models.CharField(max_length=100)
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} (by {self.user.username})"

# This signal ensures every user gets a token automatically upon creation    
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        # Create a token for the new user if one doesn't already exist
        Token.objects.get_or_create(user=instance)