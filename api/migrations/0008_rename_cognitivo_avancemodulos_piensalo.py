# Generated by Django 4.0 on 2022-08-08 03:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_avancemodulos_fecha'),
    ]

    operations = [
        migrations.RenameField(
            model_name='avancemodulos',
            old_name='cognitivo',
            new_name='piensalo',
        ),
    ]