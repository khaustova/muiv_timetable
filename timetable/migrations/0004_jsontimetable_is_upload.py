# Generated by Django 4.2.6 on 2023-10-25 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0003_alter_jsontimetable_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='jsontimetable',
            name='is_upload',
            field=models.BooleanField(blank=True, null=True, verbose_name='Данные загружены'),
        ),
    ]
