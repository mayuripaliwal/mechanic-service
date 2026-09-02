from rest_framework import serializers
from .models import Mechanic

# Serializer for mechanic model
class MechanicSerializer(serializers.ModelSerializer):
    class Meta:
        model=Mechanic
        fields="__all__"