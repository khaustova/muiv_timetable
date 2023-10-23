from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .utils import filter_by_day

from datetime import datetime, timedelta
from json import loads

from .models import Group, Timetable, Tutor, Subject, Classroom, WorkType, JsonTimetable


def context(request):
    """
    Принимает параметры из строки запроса и формирует данные для передачи в шаблон:
    1) group_num, tutor, one_date, from_date, to_date - параметры из строки запроса;
    2) groups, tutors, classrooms, subjects, work_types - все существующие объекты соответствующих моделей;
    3) is_exists - существует ли расписание для группы или преподавателя;
    4) is_group - расписание запрошено для группы (True) или преподавателя (False);
    5) timetable_by_days - словарь со сформированным расписанием, где ключи - запрошенные даты, значения - всё расписание на каждую из них;
    6) today - сегодняшняя дата;
    7) week - текущая учебная неделя.
    """
    groups = Group.objects.all()
    tutors = Tutor.objects.all() 
    classrooms = Classroom.objects.all()
    subjects = Subject.objects.all()
    work_types = WorkType.objects.all()
    
    group_num = request.GET.get("select_group")
    tutor = request.GET.get("select_tutor")
    one_date = request.GET.get("one_date")
    from_date = request.GET.get("from_date")
    to_date = request.GET.get("to_date")
    
    is_exists = False
    is_group = True
    
    """ timetable - всё сушествующее расписание в соответствии с группой или преподавателем. """
    if group_num:  
        timetable = Timetable.objects.filter(group__group_num=group_num)
    else:
        timetable = Timetable.objects.filter(tutor__tutor_name=tutor)
    
    """ Если переданы две даты из диапазона, то timetable фильтруется по ним, иначе только по одной дате,
    которая по умолчанию равна сегодняшней. """   
    if from_date and to_date:
        timetable_by_days = filter_by_day(from_date, to_date, timetable)
    else:
        timetable_by_days = filter_by_day(one_date, one_date, timetable)
     
    if (group_num or tutor) and timetable.exists():
        is_exists = True
        
    if tutor:
        is_group = False
        
    today = datetime.now().date()
    week = datetime.today().isocalendar()[1]
    delta_week = 34 if week >= 48 else 7
    
    context = {
        "groups": groups,
        "tutors": tutors,
        "classrooms": classrooms,
        "subjects": subjects,
        "work_types": work_types,
        "is_exists": is_exists,
        "is_group": is_group,
        "tutor": tutor,
        "group_num": group_num,
        "from_date": from_date,
        "to_date": to_date,
        "timetable_by_days": timetable_by_days,
        "today": today,
        "week": week - delta_week,
        }     
    return context
