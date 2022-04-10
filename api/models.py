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


class Encuesta(models.Model):
    id_encuesta = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45)
    descripcion = models.TextField(blank=True, null=True)
    # Field name made lowercase.
    colorhex = models.CharField(db_column='colorHex', max_length=30)

    class Meta:
        managed = False
        db_table = 'encuesta'


class Pregunta(models.Model):
    id_pregunta = models.AutoField(primary_key=True)
    id_encuesta = models.ForeignKey(
        Encuesta, models.DO_NOTHING, db_column='id_encuesta')
    pregunta = models.TextField()
    # Field name made lowercase.
    itemid = models.IntegerField(db_column='itemID', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pregunta'


class PreguntaRespuesta(models.Model):
    id_respuesta = models.ForeignKey(
        'Respuesta', models.DO_NOTHING, db_column='id_respuesta')
    id_pregunta = models.ForeignKey(
        Pregunta, models.DO_NOTHING, db_column='id_pregunta')
    id_pregunta_respuesta = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'pregunta_respuesta'


class Respuesta(models.Model):
    id_respuesta = models.AutoField(primary_key=True)
    valor = models.IntegerField(blank=True, null=True)
    respuesta = models.CharField(max_length=60)

    class Meta:
        managed = False
        db_table = 'respuesta'


class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usuario'


class UsuarioEncuesta(models.Model):
    id_usuario_encuesta = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(
        Usuario, models.DO_NOTHING, db_column='id_usuario')
    id_encuesta = models.ForeignKey(
        Encuesta, models.DO_NOTHING, db_column='id_encuesta')
    fecha = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usuario_encuesta'


class UsuarioRespuesta(models.Model):
    id_usuario_respuesta = models.AutoField(primary_key=True)
    id_usuario_encuesta = models.ForeignKey(
        UsuarioEncuesta, models.DO_NOTHING, db_column='id_usuario_encuesta')
    id_pregunta_respuesta = models.ForeignKey(
        PreguntaRespuesta, models.DO_NOTHING, db_column='id_pregunta_respuesta')

    class Meta:
        managed = False
        db_table = 'usuario_respuesta'
