# Generated by Django 4.2.1 on 2023-05-19 08:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('homeworks', '0002_homework_points_alter_homework_full_test_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='homework',
            options={'ordering': ('-creation_date',)},
        ),
        migrations.AlterField(
            model_name='homework',
            name='creation_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
