from django.shortcuts import render
from rest_framework import generics, viewsets
# from .models import Timetable
# from .serializers import TimetableSerializer, TodoSerializer


# class TimetableAPI(generics.ListAPIView):
#     serializer_class = TimetableSerializer

#     def get_queryset(self):
#         if 'subject' in self.request.query_params:
#             return Timetable.objects.filter(subject=self.request.query_params['subject'])
#         return Timetable.objects.all()
    
# class TimetableViewSet(viewsets.ModelViewSet):
#     serializer_class = TimetableSerializer
#     queryset = Timetable.objects.all()

    # def get_queryset(self):
    #     if 'subject' in self.request.query_params:
    #         return Timetable.objects.filter(subject=self.request.query_params['subject'])
    #     return Timetable.objects.all()

    # def perform_create(self, serializer):
    #     # ensure current user is correctly populated on new objects
    #     serializer.save(user=self.request.user)
