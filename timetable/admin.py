from django.contrib import admin
from . models import Timetable, Classroom, Subject, Group, WorkType, Tutor, JsonTimetable

admin.site.register(Classroom)
admin.site.register(Subject)
admin.site.register(Group)
admin.site.register(Tutor)
admin.site.register(Timetable)
admin.site.register(WorkType)
admin.site.register(JsonTimetable)

admin.site.site_title = "Администрирование расписания в университете"
admin.site.site_header = "Администрирование расписания в университете"
