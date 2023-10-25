from django.shortcuts import render
from rest_framework import generics, viewsets
from timetable.models import Timetable
from .serializers import TimetableSerializer


class TimetableAPI(generics.ListAPIView):
    serializer_class = TimetableSerializer

    def get_queryset(self):
        if 'group' in self.request.query_params:
            return Timetable.objects.filter(group__group_num=self.request.query_params['group'])
        elif 'tutor' in self.request.query_params:
            return Timetable.objects.filter(tutor__tutor_name=self.request.query_params['tutor'])
        
        return Timetable.objects.all()
