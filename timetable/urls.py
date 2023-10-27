from django.urls import path
from django.views.generic import TemplateView

app_name = 'timetable'

urlpatterns = [
    path('', TemplateView.as_view(template_name='timetable/index.html'), name='home'),
]
