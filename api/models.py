from enum import unique
from django.db import models
from cloudinary.models import CloudinaryField
from django.utils.text import slugify
import hashlib


class Personal(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)
    funcion = models.TextField()
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    foto = CloudinaryField("Image", overwrite=True, format="jpg")

    class Meta:
        ordering = ("-creado",)

    def __str__(self):
        return self.nombre


class Sexo(models.Model):
    id = models.AutoField(primary_key=True)
    sexo = models.CharField(max_length=200)

    def __str__(self):
        return self.sexo


class Estado_Civil(models.Model):
    id = models.AutoField(primary_key=True)
    estado_civil = models.CharField(max_length=200)

    def __str__(self):
        return self.estado_civil


class Escolaridad(models.Model):
    id = models.AutoField(primary_key=True)
    escolaridad = models.CharField(max_length=200)

    def __str__(self):
        return self.escolaridad


