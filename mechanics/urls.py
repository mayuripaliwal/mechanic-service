from django.urls import path
from .views import MechanicListView, MechanicDetailView

urlpatterns = [
    path('mechanics/',MechanicListView.as_view()),
    path('mechanics/<int:id>/',MechanicDetailView.as_view())
]
