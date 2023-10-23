from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import path, include


def page_not_found_handler(request: HttpRequest, exception=None) -> HttpResponse:
    return render(request, 'timetable/404.html')


def server_error_handler(request: HttpRequest, exception=None) -> HttpResponse:
    return render(request, 'timetable/500.html')


handler404 = page_not_found_handler
handler500 = server_error_handler

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('timetable.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
]

if bool(settings.DEBUG):
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)