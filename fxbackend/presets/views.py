from rest_framework import viewsets
from .models import Preset
from .serializers import PresetSerializer

# We use Django’s ModelViewSet to handle all CRUD operations in one go.

# ViewSet provides built-in GET, POST, PUT, DELETE operations for Presets.
class PresetViewSet(viewsets.ModelViewSet):
    # This tells Django to return all Preset records, newest first.
    queryset = Preset.objects.all().order_by('-created_at')

    # This tells Django to use our serializer to convert model ↔ JSON.
    serializer_class = PresetSerializer