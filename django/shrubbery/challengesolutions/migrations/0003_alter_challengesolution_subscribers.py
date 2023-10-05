# Generated by Django 4.2.1 on 2023-10-05 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_user_email_notification_solution_comments'),
        ('challengesolutions', '0002_challengesolution_subscribers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='challengesolution',
            name='subscribers',
            field=models.ManyToManyField(blank=True, related_name='subscribed_challenges', to='users.teacher'),
        ),
    ]
