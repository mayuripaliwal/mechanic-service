from django.urls import path
from .views import MechanicListView, MechanicDetailView, ServiceRequestView

urlpatterns = [
    path('mechanics/',MechanicListView.as_view()),
    path('mechanics/<int:id>/',MechanicDetailView.as_view()),
    path('service-requests/',ServiceRequestView.as_view())
]
