# Generated by Django 4.0 on 2022-07-04 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_rename_diagnostico_avancemodulos_autoevaluativo'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProgramaAcademico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('facultad', models.CharField(max_length=100)),
                ('nivel', models.CharField(max_length=100)),
                ('programa', models.CharField(max_length=200)),
            ],
        ),
    ]
