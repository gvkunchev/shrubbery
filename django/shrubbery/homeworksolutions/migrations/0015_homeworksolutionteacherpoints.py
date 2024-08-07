# Generated by Django 4.2.1 on 2023-05-29 08:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('homeworksolutions', '0014_homeworksolutionhistoryinlinecomment'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomeworkSolutionTeacherPoints',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.IntegerField(default=0)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('solution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homeworksolutions.homeworksolution')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
