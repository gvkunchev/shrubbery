# Generated by Django 4.2.1 on 2023-05-29 10:15

import challengesolutions.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('challenges', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChallengeSolution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.FileField(upload_to=challengesolutions.models.get_upload_path, validators=[challengesolutions.models.validate_py_extension])),
                ('upload_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('points', models.IntegerField(default=0)),
                ('result', models.TextField(default='')),
                ('passed_tests', models.IntegerField(default=0)),
                ('failed_tests', models.IntegerField(default=0)),
                ('line_count', models.IntegerField(default=0)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('challenge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='challenges.challenge')),
            ],
            options={
                'ordering': ('-upload_date',),
            },
        ),
        migrations.CreateModel(
            name='ChallengeSolutionHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.FileField(upload_to=challengesolutions.models.get_history_upload_path, validators=[challengesolutions.models.validate_py_extension])),
                ('upload_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('diff', models.TextField(default='')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('challenge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='challenges.challenge')),
                ('solution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='challengesolutions.challengesolution')),
            ],
            options={
                'ordering': ('-upload_date',),
            },
        ),
        migrations.CreateModel(
            name='ChallengeSolutionTeacherPoints',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.IntegerField(default=0)),
                ('solution', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='challengesolutions.challengesolution')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ChallengeSolutionInlineComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('content', models.TextField()),
                ('line', models.IntegerField()),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('solution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='challengesolutions.challengesolution')),
            ],
            options={
                'ordering': ('line', 'date'),
            },
        ),
        migrations.CreateModel(
            name='ChallengeSolutionHistoryInlineComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('content', models.TextField()),
                ('line', models.IntegerField()),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('history', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='challengesolutions.challengesolutionhistory')),
                ('solution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='challengesolutions.challengesolution')),
            ],
            options={
                'ordering': ('line', 'date'),
            },
        ),
        migrations.CreateModel(
            name='ChallengeSolutionComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.IntegerField(default=0)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('content', models.TextField()),
                ('starred', models.BooleanField(default=False)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('solution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='challengesolutions.challengesolution')),
            ],
            options={
                'ordering': ('-date',),
            },
        ),
    ]
