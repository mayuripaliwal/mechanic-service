from django.shortcuts import render
from rest_framework.views import APIView
from .models import Mechanic
from .serializers import MechanicSerializer
from rest_framework.response import Response

# Create your views here.
class MechanicListView(APIView):
    def get(self,request):
        mechanics=Mechanic.objects.all()

        serializer=MechanicSerializer(mechanics,many=True)

        return Response(serializer.data)
