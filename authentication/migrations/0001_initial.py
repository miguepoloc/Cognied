# Generated by Django 4.0.1 on 2022-02-25 23:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('api', '0012_delete_usuarios'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usuarios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document', models.BigIntegerField(db_index=True, unique=True)),
                ('password', models.CharField(max_length=100)),
                ('email', models.EmailField(db_index=True, max_length=254, unique=True)),
                ('nombre', models.TextField(max_length=200)),
                ('tipo_documento', models.CharField(blank=True, choices=[('PA', 'PA'), ('CE', 'CE'), ('CC', 'CÉDULA DE CIUDADANÍA'), ('TI', 'TI'), ('RC', 'RC')], default='CC', max_length=2, null=True)),
                ('lugar_nacimiento', models.TextField(blank=True, max_length=200, null=True)),
                ('ocupacion', models.TextField(blank=True, max_length=200, null=True)),
                ('ciudad_residencia', models.TextField(blank=True, max_length=200, null=True)),
                ('estrato', models.IntegerField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('escolaridad', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.escolaridad')),
                ('estado_civil', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.estado_civil')),
                ('sexo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.sexo')),
            ],
        ),
    ]
