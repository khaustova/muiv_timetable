from django.urls import path
from django.views.generic import TemplateView
from .views import TimetableAPI

urlpatterns = [
    path('timetable/', TimetableAPI.as_view(), name='timetable_api'),
]