# Generated by Django 4.2.1 on 2023-10-05 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_user_email_notification_solution_comments'),
        ('homeworksolutions', '0019_alter_homeworksolution_subscribers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homeworksolution',
            name='subscribers',
            field=models.ManyToManyField(blank=True, related_name='subscribed_homeworks', to='users.teacher'),
        ),
    ]
