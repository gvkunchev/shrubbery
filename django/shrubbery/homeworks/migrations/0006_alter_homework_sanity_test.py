# Generated by Django 4.2.1 on 2023-05-25 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homeworks', '0005_homework_executing_tests'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homework',
            name='sanity_test',
            field=models.TextField(default='1'),
            preserve_default=False,
        ),
    ]