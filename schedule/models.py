from django.db import models

class Timetable(models.Model):
    work_day = models.DateField()
    subject = models.CharField(max_length=256, verbose_name='Предмет')
    
    class Meta:
        ordering = ("work_day",)

    def __str__(self):
        return self.subject
