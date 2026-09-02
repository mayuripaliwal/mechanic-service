from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from .models import Mechanic
from .serializers import MechanicSerializer
from rest_framework.response import Response

# Create your views here.
class MechanicListView(APIView):
    #this api returns all mechanics
    def get(self,request):
        mechanics=Mechanic.objects.all()

        serializer=MechanicSerializer(mechanics,many=True)

        return Response(serializer.data)

class MechanicDetailView(APIView):
    #this api returns mechanic for a given id
    def get(self,request,id):
        # if exist, return mechanic for the given id
        # else return 404
        mechanic=get_object_or_404(Mechanic,id=id)
        serializer=MechanicSerializer(mechanic)

        return Response(serializer.data)

    
