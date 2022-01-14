# Generated by Django 4.0.1 on 2022-01-14 22:33

import cloudinary.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Personal',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=200)),
                ('funcion', models.TextField()),
                ('creado', models.DateTimeField(auto_now_add=True)),
                ('actualizado', models.DateTimeField(auto_now=True)),
                ('foto', cloudinary.models.CloudinaryField(max_length=255, verbose_name='Image')),
                ('slug', models.SlugField(blank=True, max_length=255, null=True)),
            ],
            options={
                'ordering': ('-creado',),
            },
        ),
    ]