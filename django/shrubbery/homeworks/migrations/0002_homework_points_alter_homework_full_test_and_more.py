# Generated by Django 4.2.1 on 2023-05-19 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homeworks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='homework',
            name='points',
            field=models.IntegerField(default=10),
        ),
        migrations.AlterField(
            model_name='homework',
            name='full_test',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='homework',
            name='hidden',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='homework',
            name='sanity_test',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]
