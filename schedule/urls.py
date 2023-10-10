from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
   path("api/v1/timetablelist/", views.TimetableAPI.as_view(), name="timetableapi"),
]
