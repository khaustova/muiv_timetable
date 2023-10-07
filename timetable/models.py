from django.db import models

class Classroom(models.Model): 
    """
    Определяет аудитории:
    place - номер аудитории.
    """
    place = models.CharField(max_length=20)
    
    class Meta:
        ordering = ("place",)

    def __str__(self):
        return "%s" % (self.place)


class Subject(models.Model): 
    """
    Определяет дисциплины:
    subject_name - название дициплины;
    tutor - преподаватель дисцплины.
    """
    subject_name = models.CharField(max_length=100)
    tutor = models.ManyToManyField("Tutor")
    
    class Meta:
        ordering = ("subject_name",)

    def __str__(self):
        return "%s" % (self.subject_name)


class Group(models.Model): 
    """
    Определяет группы:
    group_num - номер группы;
    students - количество студентов в ней.
    """
    group_num = models.CharField(max_length=50)
    students = models.IntegerField(default=0)

    class Meta:
        ordering = ("group_num",)
    
    def __str__(self):
        return "%s" % (self.group_num)
    

class Tutor(models.Model):
    """
    Определяет преподавателей:
    tutor_name - ФИО преподавателя.
    """
    tutor_name = models.CharField(max_length=150)
    
    class Meta:
        ordering = ("tutor_name",)

    def __str__(self):
        return "%s" % self.tutor_name
    
    
class WorkType(models.Model):
    """
    Определяет тип занятий:
    work_type - тип занятий.
    """
    work_type = models.CharField(max_length=150)
    
    class Meta:
        ordering = ("work_type",)

    def __str__(self):
        return "%s" % self.work_type


class Timetable(models.Model):
    """
    Определяет расписание на определенный день и промежуток времени:
    work_day - день занятия;
    work_start - время начала занятия;
    work_end - время окончания занятия;
    tutor - преподаватель;
    classroom - аудитория;
    group - номер группы;
    subject - дисциплина;
    work_type - тип занятия.
    """
    work_day = models.DateField()
    work_start = models.TimeField()
    work_end = models.TimeField()
    tutor = models.ForeignKey("Tutor", on_delete=models.CASCADE)
    classroom = models.ForeignKey("Classroom", on_delete=models.CASCADE, null=True)
    group = models.ForeignKey("Group", on_delete=models.CASCADE)
    subject = models.ForeignKey("Subject", on_delete=models.CASCADE)
    work_type = models.ForeignKey("WorkType", on_delete=models.CASCADE)
    
    class Meta:
        ordering = ("work_day",)

    def __str__(self):
        return "%s - (%s-%s) - %s" % (self.work_day, self.work_start, self.work_end, self.group)
    
    
class JsonTimetable(models.Model):
    """
    Определяет хранение загруженных файлов:
    json_file - загруженный файл;
    date_time_of_upload - время загрузки (заполняется автоматически).
    """
    json_file = models.FileField(upload_to="uploads/")
    date_time_of_upload = models.DateTimeField(auto_now = True)
    
    def __str__(self):
        return "%s" % self.json_file
    
    