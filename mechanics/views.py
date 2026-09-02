from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from .models import Mechanic
from .serializers import MechanicSerializer
from rest_framework.response import Response
from rest_framework import status
from .serializers import ServiceRequestSerializer
# Create your views here.

class MechanicListView(APIView):
    #this api returns all mechanics
    def get(self,request):
        mechanics=Mechanic.objects.all()

        serializer=MechanicSerializer(mechanics,many=True)

        return Response(serializer.data)
    
    #this api adds a new mechanic to the db
    def post(self,request):
        serializer=MechanicSerializer(data=request.data)

        # if request is valid, add the mechanic to db and return the added details
        # return 201
        if serializer.is_valid():
            
            serializer.save()

            return Response(serializer.data,status=201)

        # if request is not valid, return 400
        return Response(serializer.errors,status=400)

class MechanicDetailView(APIView):
    #this api returns mechanic for a given id
    def get(self,request,id):
        # if exist, return mechanic for the given id
        # else return 404

        try:
            mechanic=Mechanic.objects.get(id=id)
        except Mechanic.DoesNotExist:
            return Response(
                {"detail":f"Mechanic with id {id} does not exist."},
                status=404)
        
        serializer=MechanicSerializer(mechanic)

        return Response(serializer.data)

    # this api updates the mechanic details for a given mechanic id
    def put(self,request,id):
        # first check does this mechanic exist
        # if mechanic exists, then update details and return 200
        # if mechanic does not exist, return 404
        # if request is not valid, return 400
        try: 
            mechanic=Mechanic.objects.get(id=id)
        except Mechanic.DoesNotExist:
            return Response(
                {"detail":f"Mechanic with id {id} does not exist."},
                status=404
                )

        serializer=MechanicSerializer(mechanic,data=request.data)
        
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)

        return Response(serializer.errors,status=400)

    # this api does partial update on mechanic details for a given mechanic id
    def patch(self,request,id):
        try:
            mechanic=Mechanic.objects.get(id=id)
        except Mechanic.DoesNotExist:
            return Response(
                {"detail":f"Mechanic with id {id} does not exist."},
                status=404
            )
        

        serializer=MechanicSerializer(mechanic,data=request.data,partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)

        return Response(serializer.errors,status=400)


    # this api deletes the mechanic for a given mechanic id
    def delete(self,request,id):
        #first check if the id exists in db
        #if exist, delete the record and return 204
        #else return 404
        try:
            mechanic=Mechanic.objects.get(id=id)
        except Mechanic.DoesNotExist:
            return Response(
                {"detail":f"Mechanic with id {id} does not exist."},
                status=404
            )
        
        mechanic.delete()

        return Response(status=204)


#API for service requests
class ServiceRequestView(APIView):
    #this api creates a new service request
    def post(self,request):
        #first check is this a valid request
        serializer=ServiceRequestSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data,status=201)
        
        return Response(serializer.errors,status=400)


    
