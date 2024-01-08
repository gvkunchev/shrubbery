# Generated by Django 4.2.1 on 2024-01-08 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0005_action_forced_seen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='type',
            field=models.CharField(blank=True, choices=[('NA', 'News Article'), ('F', 'Forum'), ('FC', 'Forum Comment'), ('HW', 'Homework'), ('HWC', 'Homework Comment'), ('HWS', 'Homework Solution'), ('HWSU', 'Homework Solution Update'), ('HWSC', 'Homework Solution Comment'), ('HWSIC', 'Homework Solution Inline Comment'), ('C', 'Challenge'), ('CC', 'Challenge Comment'), ('CS', 'Challenge Solution'), ('CSU', 'Challenge Solution Update'), ('CSC', 'Challenge Solution Comment'), ('FSC', 'Final Schedule flip')], default=None, max_length=5, null=True),
        ),
    ]