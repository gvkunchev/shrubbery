# Generated by Django 4.2.1 on 2023-05-29 08:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homeworksolutions', '0016_alter_homeworksolutionteacherpoints_solution'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='homeworksolutionteacherpoints',
            name='author',
        ),
    ]