from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("timetable/", views.timetable, name="timetable"),

    path("admin/", admin.site.urls),
    
    # path("manager/", views.manager, name="manager"),
    
    # path("manager/upload", views.upload, name="upload"),
    
    # path("manager/create-timetable", views.create_timetable, name="create_timetable"),
    # path("manager/edit-timetable/<int:id>/", views.edit_timetable, name="edit-timetable"),
    # path("manager/delete-timetable/<int:id>/", views.delete_timetable, name="delete-timetable"),
    
    # path("manager/timetable-objects", views.timetable_objects, name="timetable_objects"),
    
    # path("manager/create-group", views.create_group, name="create_group"),
    # path("manager/edit-group/<int:id>/", views.edit_group, name="edit_group"),
    # path("manager/delete-group/<int:id>/", views.delete_group, name="delete_group"),
    
    # path("manager/create-tutor", views.create_tutor, name="create_tutor"),
    # path("manager/edit-tutor/<int:id>/", views.edit_tutor, name="edit_tutor"),
    # path("manager/delete-tutor/<int:id>/", views.delete_tutor, name="delete_tutor"),
    
    # path("manager/create-subject", views.create_subject, name="create_subject"),
    # path("manager/edit-subject/<int:id>/", views.edit_subject, name="edit_subject"),
    # path("manager/delete-subject/<int:id>/", views.delete_subject, name="delete_subject"),
    
    # path("manager/create-work-type", views.create_work_type, name="create_work_type"),
    # path("manager/edit-work-type/<int:id>/", views.edit_work_type, name="edit_work_type"),
    # path("manager/delete-work-type/<int:id>/", views.delete_work_type, name="delete_work_type"),
    
    # path("manager/create-classroom", views.create_classroom, name="create_classroom"),
    # path("manager/edit-classroom/<int:id>/", views.edit_classroom, name="edit_classroom"),
    # path("manager/delete-classroom/<int:id>/", views.delete_classroom, name="delete_classroom"),
    
]

if settings.DEBUG: 
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
