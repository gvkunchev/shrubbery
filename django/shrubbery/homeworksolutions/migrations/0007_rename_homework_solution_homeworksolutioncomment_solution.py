# Generated by Django 4.2.1 on 2023-05-22 10:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homeworksolutions', '0006_homeworksolutioncomment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='homeworksolutioncomment',
            old_name='homework_solution',
            new_name='solution',
        ),
    ]
