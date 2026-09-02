from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
# Create your models here.
# Model for mechanic table
class Mechanic(models.Model):
    id=models.BigAutoField(primary_key=True)
    name=models.CharField(max_length=100)
    phone=models.CharField(max_length=10)
    location=models.CharField(max_length=255)
    rating=models.DecimalField(
        max_digits=2,
        decimal_places=1,
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(5.0)
        ]
    )
    is_open=models.BooleanField(default=True)
    services=models.JSONField(default=list)

# Model for service requests
class ServiceRequest(models.Model):
    id=models.BigAutoField(primary_key=True)
    customer_name=models.CharField(max_length=100)
    customer_phone=models.CharField(max_length=10)
    vehicle_number=models.CharField(max_length=20)
    mechanic=models.ForeignKey(Mechanic,on_delete=models.CASCADE)
    service=models.CharField(max_length=50)
    problem_description=models.TextField()
    status=models.CharField(max_length=20,default="PENDING")
    created_at=models.DateTimeField(auto_now_add=True)


    