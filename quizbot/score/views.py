from django.db.models import F
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ScoreSerializer
from .models import Score
class UpdateScore(APIView):
   
   def post(self, request , format = None):
       
       serilizer = ScoreSerializer(data=request.data)
       if serilizer.is_valid():
           name = serilizer.validated_data['name']
           points = serilizer.validated_data['points']
           
           if Score.objects.filter(name=name).exists():
               serilizer = Score.objects.get(name=name)
               serilizer.points = F('points') + points
        
           serilizer.save()  
           return Response(None , status=status.HTTP_201_CREATED)
       return Response(serilizer.errors, status=status.HTTP_400_BAD_REQUEST)
   
   

class Leaderboard(APIView):

    def get(self, request, formate=None, **kwargs):
        scores = Score.objects.all().order_by('-points')[:10]
        serializer = ScoreSerializer(scores, many=True)
        return Response(serializer.data)     