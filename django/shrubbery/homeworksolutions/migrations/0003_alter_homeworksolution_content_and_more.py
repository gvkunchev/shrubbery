# Generated by Django 4.2.1 on 2023-05-19 12:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import homeworksolutions.models


class Migration(migrations.Migration):

    dependencies = [
        ('homeworks', '0004_homeworkcomment'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('homeworksolutions', '0002_alter_homeworksolution_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homeworksolution',
            name='content',
            field=models.FileField(upload_to=homeworksolutions.models.get_upload_path, validators=[homeworksolutions.models.validate_py_extension]),
        ),
        migrations.CreateModel(
            name='HomeworkSolutionHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.FileField(upload_to=homeworksolutions.models.get_history_upload_path, validators=[homeworksolutions.models.validate_py_extension])),
                ('upload_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('homework', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homeworks.homework')),
            ],
            options={
                'ordering': ('-upload_date',),
            },
        ),
        migrations.AddField(
            model_name='homeworksolution',
            name='history',
            field=models.ManyToManyField(to='homeworksolutions.homeworksolutionhistory'),
        ),
    ]
