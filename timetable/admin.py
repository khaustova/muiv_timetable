from django.contrib import admin
from .utils import upload_data
from .models import Timetable, Classroom, Subject, Group, WorkType, Tutor, JsonTimetable


@admin.register(Tutor)
class TutorAdmin(admin.ModelAdmin):
    list_display = ('tutor_name',)
    search_fields = ('tutor_name',)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('group_num',)
    search_fields = ('group_num',)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('subject_name',)
    search_fields = ('subject_name',)



@admin.register(WorkType)
class WorkTypeAdmin(admin.ModelAdmin):
    list_display = ('work_type',)
    search_fields = ('work_type',)


@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('place',)
    search_fields = ('place',)


@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    list_display = (
        'work_day',
        'work_start',
        'work_end',
        'tutor',
        'subject',
        'work_type',
        'group',
        'classroom'
    )
    list_filter = ('work_day', 'tutor', 'group', 'subject', 'classroom', 'work_type')
    search_fields = (
        'work_day',
        'work_start',
        'work_end',
        'tutor__tutor_name',
        'group__group_num',
        'subject__subject_name',
        'work_type__work_type',
        'classroom__place'
    )
    autocomplete_fields = ['tutor', 'group', 'subject', 'work_type', 'classroom']


@admin.register(JsonTimetable)
class JsonTimeTableAdmin(admin.ModelAdmin):
    fields = ('json_file',)
    list_display = ('json_file', 'date_time_of_upload', 'is_upload', 'message')
    list_filter = ('is_upload',)

    def save_model(self, request, obj, form, change):
        result = upload_data(obj)
        obj.is_upload, obj.message = result['is_upload'], result['message']
        super().save_model(request, obj, form, change)
