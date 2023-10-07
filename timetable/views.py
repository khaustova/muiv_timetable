from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from datetime import datetime, timedelta
from json import loads

from .models import Group, Timetable, Tutor, Subject, Classroom, WorkType, JsonTimetable


def index(request):
    """ 
    Перенаправляет с главной страницы на страницу /timetable.
    """
    return HttpResponseRedirect("timetable")


def timetable(request):
    """ 
    Получает данные из функции get_context_for_timetable() и выводит главную страницу с расписанием.
    """
    context = get_context_for_timetable(request)
    return render(request, "index.html", context) 


def get_context_for_timetable(request):
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


def daterange(start_date, end_date):
    """
    Принимает начальную и конечную дату, генерирует даты из данного промежутка.
    Используется для формирования словаря с расписанием по дням.
    """
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def filter_by_day(from_date, to_date, timetable):
    """
    Принимает две даты, обозначающие начало заданного периода, и расписание, которое фильтрует в соответствии с ними.
    Возвращает словарь, где ключи - даты, полученные из функции daterange(), значения - отфильтрованное по ним расписание.
    """
    if from_date:
        timetable = timetable.filter(work_day__gte=from_date)
    if to_date:
        timetable = timetable.filter(work_day__lte=to_date) 
               
    timetable_days = {}
    start = datetime.strptime(from_date, "%Y-%m-%d").date() if from_date else datetime.now().date()
    end = datetime.strptime(to_date, "%Y-%m-%d").date() if to_date else datetime.now().date()
    for single_date in daterange(start, end + timedelta(days=1)):
        timetable_days[single_date] = timetable.filter(work_day=single_date)
    return timetable_days


@login_required
def manager(request):
    """ 
    Получает данные из функции get_context_for_timetable() и выводит страницу для управления расписанием.
    """
    context = get_context_for_timetable(request)
    return render(request, "timetable_manager.html", context)


def upload(request):
    """ 
    Загружает json-файл с расписанием на сервер и обрабатывает его с помощью функции json_to(), получая само расписание в виде
    словаря, где ключ - дата, значение - расписание на неё, а также множества, содержащие все объекты расписания.
    Для каждого из расписания и объектов расписания проверяет его существование во всех объектах модели, и если его не существует, 
    то создаёт новый объект.
    """
    if request.method == "POST":
        uploadedFile = request.FILES["json_file"]
        file = JsonTimetable(json_file = uploadedFile)
        file.save()
        
        timetable, all_tutors, all_subjects, all_groups, all_classrooms, all_work_types = json_to(file.json_file)

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

    return render(request, "upload.html")


def json_to(file): 
    """
    Принимает json-файл, который преобразует в объект Python и на его основе формирует словарь с расписанием по датам.
    """
    scheduler = loads(file.read())
    timetable = {}
    all_tutors, all_subjects, all_groups, all_classrooms, all_work_types = set(), set(), set(), set(), set()
    for one_day in scheduler["sheduler"]:
        year, month, day = str(one_day["workYear"]), str(one_day["workMonth"]), str(one_day["workDate"])
        dt = datetime.strptime(year + month + day, "%Y%m%d").date()
        timetable[dt] = []
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
                timetable[dt].append(daily_routine)
            else:
                for group in groups_temp:         
                    daily_routine["group"] = group
                    timetable[dt].append(daily_routine.copy())
                    
    return timetable, all_tutors, all_subjects, all_groups, all_classrooms, all_work_types


@login_required
def create_timetable(request):
    """ 
    Создаёт новое расписание как новый объект соответствующей модели.
    """
    context = get_context_for_timetable(request)
    if request.method == "POST":
        timetable = Timetable()
        timetable.work_day = request.POST.get("work_day")
        timetable.work_start = request.POST.get("work_start")
        timetable.work_end = request.POST.get("work_end")
        timetable.tutor = Tutor.objects.get(tutor_name = request.POST.get("tutor"))
        timetable.group = Group.objects.get(group_num = request.POST.get("group"))
        timetable.classroom = Classroom.objects.get(place = request.POST.get("classroom"))
        timetable.subject = Subject.objects.get(subject_name = request.POST.get("subject"))
        timetable.work_type = WorkType.objects.get(work_type = request.POST.get("work_type"))      
        timetable.save()  
        return HttpResponseRedirect("/manager")
    else:
        return render(request, "create_and_edit_timetable.html", context)


@login_required
def delete_timetable(request, id):
    """ 
    Принимает id объекта модели расписания и удаляет его.
    """
    timetable = Timetable.objects.get(id=id)
    timetable.delete()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required
def edit_timetable(request, id):
    """ 
    Принимает id объекта модели расписания и редактирует его.
    При формировании страницы в соответствующих формах отображает текущие значения полей.
    """
    timetable = Timetable.objects.get(id=id)
    context = get_context_for_timetable(request)
    if request.method == "POST":
        timetable.work_day = request.POST.get("work_day")
        timetable.work_start = request.POST.get("work_start")
        timetable.work_end = request.POST.get("work_end")
        timetable.tutor = Tutor.objects.get(tutor_name = request.POST.get("tutor"))
        timetable.group = Group.objects.get(group_num = request.POST.get("group"))
        timetable.classroom = Classroom.objects.get(place = request.POST.get("classroom"))
        timetable.subject = Subject.objects.get(subject_name = request.POST.get("subject"))
        timetable.work_type = WorkType.objects.get(work_type = request.POST.get("work_type"))      
        timetable.save()  
        return HttpResponseRedirect("/manager")
    else:
        context["timetable"] = timetable
        context["tutors"] = context["tutors"].exclude(tutor_name = timetable.tutor) 
        context["subjects"] = context["subjects"].exclude(subject_name = timetable.subject) 
        context["groups"] = context["groups"].exclude(group_num = timetable.group) 
        context["classrooms"] = context["classrooms"].exclude(place = timetable.classroom) 
        context["work_types"] = context["work_types"].exclude(work_type = timetable.work_type) 
        return render(request, "create_and_edit_timetable.html", context)


@login_required
def timetable_objects(request):
    """ 
    Получает данные из функции get_context_for_timetable() и выводит страницу для управления объектами расписания.
    """
    context = get_context_for_timetable(request)
    return render(request, "timetable_objects.html", context)  


@login_required
def create_classroom(request):
    """ 
    Создаёт новую аудиторию как новый объект соответствующей модели.
    """
    context = get_context_for_timetable(request)
    context["check_classroom"] = True
    if request.method == "POST":
        classroom = Classroom(place = request.POST.get("place") )
        classroom.save()  
        return HttpResponseRedirect("/manager/timetable-objects")
    else:
        return render(request, "create_and_edit_timetable_objects.html", context)  


@login_required
def edit_classroom(request, id):
    """ 
    Принимает id объекта модели аудитории и редактирует его.
    При формировании страницы в соответствующих формах отображает текущие значения полей.
    """
    classroom = Classroom.objects.get(id=id)
    context = get_context_for_timetable(request)
    context["place"] = classroom
    context["check_classroom"] = True
    if request.method == "POST":
        classroom.place = request.POST.get("place")     
        classroom.save()  
        return HttpResponseRedirect("/manager/timetable-objects")
    else:
        return render(request, "create_and_edit_timetable_objects.html", context)  
    
    
@login_required   
def delete_classroom(request, id):
    """ 
    Принимает id объекта модели аудитории и удаляет его.
    """
    classroom = Classroom.objects.get(id=id)
    classroom.delete()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required
def create_work_type(request):
    """ 
    Создаёт новый тип занятия как новый объект соответствующей модели.
    """
    context = get_context_for_timetable(request)
    context["check_work_type"] = True
    if request.method == "POST":
        work_type = WorkType(work_type = request.POST.get("work_type") )
        work_type.save()  
        return HttpResponseRedirect("/manager/timetable-objects")
    else:
        return render(request, "create_and_edit_timetable_objects.html", context)  


@login_required
def edit_work_type(request, id):
    """ 
    Принимает id объекта модели типа занятия и редактирует его.
    При формировании страницы в соответствующих формах отображает текущие значения полей.
    """
    work_type = WorkType.objects.get(id=id)
    context = get_context_for_timetable(request)
    context["work_type"] = work_type
    context["check_work_type"] = True
    if request.method == "POST":
        work_type.work_type = request.POST.get("work_type")     
        work_type.save()  
        return HttpResponseRedirect("/manager/timetable-objects")
    else:
        return render(request, "create_and_edit_timetable_objects.html", context)  
    
    
@login_required    
def delete_work_type(request, id):
    """ 
    Принимает id объекта модели типа занятия и удаляет его.
    """
    work_type = WorkType.objects.get(id=id)
    work_type.delete()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required
def create_tutor(request):
    """ 
    Создаёт нового преподавателя как новый объект соответствующей модели.
    """
    context = get_context_for_timetable(request)
    context["check_tutor"] = True
    if request.method == "POST":
        tutor = Tutor(tutor_name = request.POST.get("tutor_name") )
        tutor.save()  
        return HttpResponseRedirect("/manager/timetable-objects")
    else:
        return render(request, "create_and_edit_timetable_objects.html", context)  


@login_required
def edit_tutor(request, id):
    """ 
    Принимает id объекта преподавателя и редактирует его.
    При формировании страницы в соответствующих формах отображает текущие значения полей.
    """
    tutor = Tutor.objects.get(id=id)
    context = get_context_for_timetable(request)
    context["tutor_name"] = tutor
    context["check_tutor"] = True
    if request.method == "POST":
        tutor.tutor_name = request.POST.get("tutor_name")     
        tutor.save()  
        return HttpResponseRedirect("/manager/timetable-objects")
    else:
        return render(request, "create_and_edit_timetable_objects.html", context)  
    
    
@login_required    
def delete_tutor(request, id):
    """ 
    Принимает id объекта модели преподавателя и удаляет его.
    """
    tutor = Tutor.objects.get(id=id)
    tutor.delete()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required
def create_subject(request):
    """ 
    Создаёт новую дисциплину как новый объект соответствующей модели.
    """
    context = get_context_for_timetable(request)
    context["check_subject"] = True
    if request.method == "POST":
        subject = Subject(subject_name = request.POST.get("subject_name") )
        subject.save()  
        return HttpResponseRedirect("/manager/timetable-objects")
    else:
        return render(request, "create_and_edit_timetable_objects.html", context)  


@login_required
def edit_subject(request, id):
    """ 
    Принимает id объекта модели дисциплины и редактирует его.
    При формировании страницы в соответствующих формах отображает текущие значения полей.
    """
    subject = Subject.objects.get(id=id)
    context = get_context_for_timetable(request)
    context["subject_name"] = subject
    context["check_subject"] = True
    if request.method == "POST":
        subject.subject_name = request.POST.get("subject_name")     
        subject.save()  
        return HttpResponseRedirect("/manager/timetable-objects")
    else:
        return render(request, "create_and_edit_timetable_objects.html", context)  
    
    
@login_required    
def delete_subject(request, id):
    """ 
    Принимает id объекта модели дисциплины и удаляет его.
    """
    subject = Subject.objects.get(id=id)
    subject.delete()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required
def create_group(request):
    """ 
    Создаёт новую группу как новый объект соответствующей модели.
    """
    context = get_context_for_timetable(request)
    context["check_group"] = True
    if request.method == "POST":
        group = Group(group_num = request.POST.get("group_num") )
        group.save()  
        return HttpResponseRedirect("/manager/timetable-objects")
    else:
        return render(request, "create_and_edit_timetable_objects.html", context)  


@login_required
def edit_group(request, id):
    """ 
    Принимает id объекта модели группы и редактирует его.
    При формировании страницы в соответствующих формах отображает текущие значения полей.
    """
    group = Group.objects.get(id=id)
    context = get_context_for_timetable(request)
    context["group_num"] = group
    context["check_group"] = True
    if request.method == "POST":
        group.group_num = request.POST.get("group_num")     
        group.save()  
        return HttpResponseRedirect("/manager/timetable-objects")
    else:
        return render(request, "create_and_edit_timetable_objects.html", context)  
    
    
@login_required    
def delete_group(request, id):
    """ 
    Принимает id объекта модели группы и удаляет его.
    """
    group = Group.objects.get(id=id)
    group.delete()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))