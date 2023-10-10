from django.shortcuts import render
from rest_framework import generics
from .models import Timetable
from .serializers import TimetableSerializer


class TimetableAPI(generics.ListAPIView):
    serializer_class = TimetableSerializer

    def get_queryset(self):
        if 'subject' in self.request.query_params:
            return Timetable.objects.filter(subject=self.request.query_params['subject'])
        return Timetable.objects.all()


    
