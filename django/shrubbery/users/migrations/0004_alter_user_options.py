# Generated by Django 4.2.1 on 2023-05-10 12:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_github_alter_user_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ('is_active', 'first_name', 'last_name')},
        ),
    ]
