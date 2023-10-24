from datetime import datetime, timedelta
from typing import Dict, Tuple, TextIO
from json import loads

from .models import Group, Timetable, Tutor, Subject, Classroom, WorkType


def daterange(start_date: datetime, end_date: datetime) -> datetime:
    """
    Принимает начальную и конечную дату, генерирует даты из данного промежутка.
    Используется для формирования словаря с расписанием по дням.
    """
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)
        
        
def filter_by_day(
    from_date: datetime, 
    to_date: datetime, 
    timetable: Timetable
    ) -> Dict[datetime, Timetable]:
    """
    Принимает две даты, обозначающие начало заданного периода, и расписание,
    которое фильтрует в соответствии с ними.
    Возвращает словарь, где ключи - даты, полученные из функции daterange(), 
    значения - отфильтрованное по ним расписание.
    """
    if from_date:
        timetable = timetable.filter(work_day__gte=from_date)
    if to_date:
        timetable = timetable.filter(work_day__lte=to_date) 
    
    start = datetime.strptime(from_date, "%Y-%m-%d").date() if from_date else datetime.now().date()
    end = datetime.strptime(to_date, "%Y-%m-%d").date() if to_date else datetime.now().date()
    
    timetable_by_days = {}
    
    for single_date in daterange(start, end + timedelta(days=1)):
        timetable_by_days[single_date] = timetable.filter(work_day=single_date)
        
    return timetable_by_days



def json_to_dict(file: TextIO) -> Tuple: 
    """
    Принимает json-файл, который преобразует в объект Python и на его основе 
    формирует словарь с расписанием по датам.
    """
    scheduler = loads(file.json_file.read())
    
    timetable = {}
    all_tutors = set()
    all_subjects = set()
    all_groups = set()
    all_classrooms = set()
    all_work_types = set()
    
    for one_day in scheduler["sheduler"]:
        year = str(one_day["workYear"])
        month = str(one_day["workDate"])
        day = str(one_day["workMonth"])
        
        date = datetime.strptime(year + month + day, "%Y%m%d").date()
        timetable[date] = []
        
        for routine in one_day["workSheduler"]:
            daily_routine = {}
            daily_routine["work_start"] = datetime.strptime(routine["workStart"], "%H:%M").time()
            daily_routine["work_end"] = datetime.strptime(routine["workEnd"], "%H:%M").time()
            daily_routine["work_type"] = routine["workType"]
            daily_routine["subject"] = routine["area"]
            daily_routine["tutor"] = routine["tutor"]
            daily_routine["classroom"] = routine["place"]
            daily_routine["hours"] = routine["hours"]
            
            all_subjects.add(daily_routine["subject"])
            all_tutors.add(daily_routine["tutor"])
            all_classrooms.add(daily_routine["classroom"])
            all_work_types.add(daily_routine["work_type"])
            
            groups_temp = []
            for groups in routine["groups"]:
                groups_temp.append(groups["groupNum"])  
                all_groups.add(groups["groupNum"])   
            if len(groups_temp) == 1:
                daily_routine["group"] = "".join(groups_temp)
                timetable[date].append(daily_routine)
            else:
                for group in groups_temp:         
                    daily_routine["group"] = group
                    timetable[date].append(daily_routine.copy())
                    
    return (
        timetable, 
        all_tutors, 
        all_subjects, 
        all_groups, 
        all_classrooms, 
        all_work_types
    )


def upload_data(file: TextIO) -> None:
    
    """ 
    Загружает json-файл с расписанием на сервер и обрабатывает его с помощью 
    функции json_to_dict(), получая само расписание в виде словаря, 
    где ключ - дата, значение - расписание на неё, а также множества, 
    содержащие все объекты расписания.
    Для каждого из расписания и объектов расписания проверяет его существование 
    во всех объектах модели, и если его не существует, то создаёт новый объект.
    """
    timetable, all_tutors, all_subjects, all_groups, all_classrooms, all_work_types = json_to_dict(file)

    for tutor in all_tutors:
        if not Tutor.objects.filter(tutor_name = tutor).exists():  
            Tutor.objects.create(tutor_name = tutor)
    
    for group in all_groups:
        if not Group.objects.filter(group_num = group).exists(): 
            Group.objects.create(group_num = group)
    
    for subject in all_subjects:
        if not Subject.objects.filter(subject_name = subject).exists(): 
            Subject.objects.create(subject_name = subject)
            
    for classroom in all_classrooms:
        if not Classroom.objects.filter(place = classroom).exists(): 
            Classroom.objects.create(place = classroom)
            
    for work_type in all_work_types:
        if not WorkType.objects.filter(work_type = work_type).exists(): 
            WorkType.objects.create(work_type = work_type)

    for date, timetables_for_date in timetable.items():
        for each_timetable in timetables_for_date:
            if not Timetable.objects.filter(
                work_start = each_timetable["work_start"],
                work_end = each_timetable["work_end"],
                work_day = date,
                tutor = Tutor.objects.get(tutor_name = each_timetable["tutor"]),
                group = Group.objects.get(group_num = each_timetable["group"]),
                classroom = Classroom.objects.get(place = each_timetable["classroom"]),
                subject = Subject.objects.get(subject_name = each_timetable["subject"]),
                work_type = WorkType.objects.get(work_type = each_timetable["work_type"]),
            ):
                Timetable.objects.create(
                work_start = each_timetable["work_start"],
                work_end = each_timetable["work_end"],
                work_day = date,
                tutor = Tutor.objects.get(tutor_name = each_timetable["tutor"]),
                group = Group.objects.get(group_num = each_timetable["group"]),
                classroom = Classroom.objects.get(place = each_timetable["classroom"]),
                subject = Subject.objects.get(subject_name = each_timetable["subject"]),
                work_type = WorkType.objects.get(work_type = each_timetable["work_type"]),
            )