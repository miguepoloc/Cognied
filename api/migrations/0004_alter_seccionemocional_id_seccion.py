# Generated by Django 4.0.1 on 2022-04-24 00:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_seccionemocional'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seccionemocional',
            name='id_seccion',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]