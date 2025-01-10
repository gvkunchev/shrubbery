# Generated by Django 4.2.1 on 2025-01-09 14:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('homeworks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='homeworkcomment',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='homeworkcomment',
            name='homework',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homeworks.homework'),
        ),
        migrations.AddField(
            model_name='homeworkcomment',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='homeworks.homeworkcomment'),
        ),
        migrations.AddField(
            model_name='homework',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]