# Generated by Django 4.2.1 on 2023-05-22 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homeworks', '0004_homeworkcomment'),
    ]

    operations = [
        migrations.AddField(
            model_name='homework',
            name='executing_tests',
            field=models.BooleanField(default=False),
        ),
    ]
