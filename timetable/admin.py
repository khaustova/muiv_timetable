from django.contrib import admin
from django.db import transaction
from .utils import upload_data
from .models import Timetable, Classroom, Subject, Group, WorkType, Tutor, JsonTimetable

admin.site.register(Classroom)
admin.site.register(Subject)
admin.site.register(Group)
admin.site.register(Tutor)
admin.site.register(WorkType)


@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    list_display = ('work_day', 'work_start', 'work_end', 'tutor', 'subject', 'work_type', 'group', 'classroom')
    list_filter = ('work_day', 'tutor', 'group', 'subject', 'classroom', 'work_type')
    

@admin.register(JsonTimetable)
class JsonTimeTableAdmin(admin.ModelAdmin):
    fields = ('json_file',)
    list_display = ('json_file', 'date_time_of_upload', 'message')
    
    def save_model(self, request, obj, form, change):
        obj.message = upload_data(obj)
        super().save_model(request, obj, form, change)
        #transaction.on_commit(lambda: upload_data(obj))
    