# Generated by Django 4.2.6 on 2023-10-25 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timetable', '0002_alter_classroom_options_alter_group_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jsontimetable',
            name='message',
            field=models.CharField(blank=True, max_length=1024, null=True, verbose_name='Сообщение'),
        ),
    ]
