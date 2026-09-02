from rest_framework import serializers
from .models import Mechanic
from .models import ServiceRequest

# Serializer for mechanic model
class MechanicSerializer(serializers.ModelSerializer):
    class Meta:
        model=Mechanic
        fields="__all__"

# Serializer for service request model
class ServiceRequestSerializer(serializers.ModelSerializer):
    mechanic_id=serializers.PrimaryKeyRelatedField(
        queryset=Mechanic.objects.all(),
        source="mechanic"
    )

    class Meta:
        model=ServiceRequest
        fields=[
            "id",
            "customer_name",
            "customer_phone",
            "vehicle_number",
            "mechanic_id",
            "service",
            "problem_description",
            "status",
            "created_at"
        ]