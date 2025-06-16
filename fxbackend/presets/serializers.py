from rest_framework import serializers
from .models import Preset

# Serializers handle converting Django models ↔ JSON (for API responses).

class PresetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Preset          # Tell the serializer which model to serialize
        fields = '__all__'      # Include all fields from the model