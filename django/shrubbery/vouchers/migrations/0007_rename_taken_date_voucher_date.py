# Generated by Django 4.2.1 on 2023-05-17 15:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vouchers', '0006_voucher_taken_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='voucher',
            old_name='taken_date',
            new_name='date',
        ),
    ]
