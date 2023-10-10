from django.shortcuts import render
from rest_framework import generics
from .models import Timetable
from .serializers import TimetableSerializer


class TimetableAPI(generics.ListAPIView):
    queryset = Timetable.objects.all()
    serializer_class = TimetableSerializer
    
