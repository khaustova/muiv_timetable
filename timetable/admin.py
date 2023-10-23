from django.contrib import admin
from django.db import transaction
from .utils import upload_data
from .models import Timetable, Classroom, Subject, Group, WorkType, Tutor, JsonTimetable

admin.site.register(Classroom)
admin.site.register(Subject)
admin.site.register(Group)
admin.site.register(Tutor)
admin.site.register(Timetable)
admin.site.register(WorkType)

admin.site.site_title = "Администрирование расписания в университете"
admin.site.site_header = "Администрирование расписания в университете"

@admin.register(JsonTimetable)
class JsonTimeTableAdmin(admin.ModelAdmin):
    list_display = ('json_file', 'date_time_of_upload',)
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change:
            transaction.on_commit(lambda: upload_data(obj))