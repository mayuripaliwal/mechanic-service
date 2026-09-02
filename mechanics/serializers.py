from rest_framework import serializers
from .models import Mechanic
from .models import ServiceRequest
import re

# Serializer for mechanic model
class MechanicSerializer(serializers.ModelSerializer):
    class Meta:
        model=Mechanic
        fields="__all__"

# Serializer for service request model
class ServiceRequestSerializer(serializers.ModelSerializer):
    mechanic_id=serializers.PrimaryKeyRelatedField(
        queryset=Mechanic.objects.all(),
        source="mechanic",
        #error message if mechanic with the given id does not exist
        error_messages={
            "does_not_exist":"Mechanic with the given id does not exist."
        }
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

    #handle invalid customer phone number
    def validate_customer_phone(self,value):
        if len(value)!=10 or not value.isdigit():
            raise serializers.ValidationError("Customer phone number must be a 10-digit number.")

        return value

    #handle invalid vehicle number
    def validate_vehicle_number(self,value):
        pattern=r"^[A-Z]{2}\d{1,2}[A-Z]{1,3}\d{4}$"
        if not re.match(pattern,value):
            raise serializers.ValidationError("Vehicle number must be in the format: XX00XX0000 (e.g., MH12AB1234).")

        return value

    #handle if this service not provided by mechanic
    def validate(self,data):
        mechanic=data["mechanic"]
        service=data["service"]

        #check if this service is provided by mechanic
        if service not in mechanic.services:
            raise serializers.ValidationError({
                "service": "This service is not provided by the selected mechanic."
            })

        return data

    