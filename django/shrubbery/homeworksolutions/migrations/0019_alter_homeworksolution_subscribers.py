# Generated by Django 4.2.1 on 2023-08-15 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_user_email_notification_solution_comments'),
        ('homeworksolutions', '0018_homeworksolution_subscribers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homeworksolution',
            name='subscribers',
            field=models.ManyToManyField(blank=True, null=True, related_name='subscribed_homeworks', to='users.teacher'),
        ),
    ]