from django.urls import path
from .views import MechanicListView

urlpatterns = [
    path('mechanics/',MechanicListView.as_view())
]
