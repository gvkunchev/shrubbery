# Generated by Django 4.2.1 on 2023-05-10 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_user_theme'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='theme',
        ),
        migrations.AddField(
            model_name='user',
            name='dark_theme',
            field=models.BooleanField(default=False),
        ),
    ]
