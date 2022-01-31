from django.db import models
from cloudinary.models import CloudinaryField
from django.utils.text import slugify


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


TIPO_DE_DOCUMENTO = [
    ("PA", 'PA'),
    ("CE", 'CE'),
    ("CC", 'CÉDULA DE CIUDADANÍA'),
    ("TI", 'TI'),
    ("RC", 'RC'),
]


class Usuario(models.Model):
    id = models.BigIntegerField(primary_key=True)


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


class Datos(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200, null=True, blank=True)
    tipo_documento = models.CharField(
        max_length=2,
        choices=TIPO_DE_DOCUMENTO,
        default="CC",
        null=True, blank=True
    )
    documento = models.BigIntegerField(null=True, blank=True)
    usuario = models.ForeignKey(
        'Usuario', on_delete=models.SET_NULL, null=True, blank=True)
    sexo = models.ForeignKey(
        'Sexo', on_delete=models.SET_NULL, null=True, blank=True)
    lugar_nacimiento = models.TextField(max_length=200, null=True, blank=True)
    estado_civil = models.ForeignKey(
        'Estado_Civil', on_delete=models.SET_NULL, null=True, blank=True)
    ocupacion = models.TextField(max_length=200, null=True, blank=True)
    escolaridad = models.ForeignKey(
        'Escolaridad', on_delete=models.SET_NULL, null=True, blank=True)
    ciudad_residencia = models.TextField(max_length=200, null=True, blank=True)
    correo = models.EmailField(null=True, blank=True)
    estrato = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return '%s (%s)' % (self.nombre, self.documento)
