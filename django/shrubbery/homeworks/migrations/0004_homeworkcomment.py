# Generated by Django 4.2.1 on 2023-05-19 09:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('homeworks', '0003_alter_homework_options_alter_homework_creation_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomeworkComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.IntegerField(default=0)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('content', models.TextField()),
                ('starred', models.BooleanField(default=False)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('homework', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homeworks.homework')),
            ],
            options={
                'ordering': ('-date',),
            },
        ),
    ]