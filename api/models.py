from enum import unique
from django.db import models
from cloudinary.models import CloudinaryField


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

    def __str__(self):
        return self.nombre


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

    def __str__(self):
        return self.pregunta


class PreguntaRespuesta(models.Model):
    id_pregunta_respuesta = models.AutoField(primary_key=True)
    id_respuesta = models.ForeignKey(
        'Respuesta', models.DO_NOTHING, db_column='id_respuesta')
    id_pregunta = models.ForeignKey(
        Pregunta, models.DO_NOTHING, db_column='id_pregunta')
    orden = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'pregunta_respuesta'

    def __str__(self):
        return '%s' % (self.id_pregunta_respuesta)


class Respuesta(models.Model):
    id_respuesta = models.AutoField(primary_key=True)
    valor = models.IntegerField(blank=True, null=True)
    respuesta = models.CharField(max_length=60)

    class Meta:
        managed = False
        db_table = 'respuesta'

    def __str__(self):
        return '%s' % (self.respuesta)


class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usuario'

    def __str__(self):
        return '%s' % (self.nombre)


class UsuarioEncuesta(models.Model):
    id_usuario_encuesta = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(
        Usuario, models.DO_NOTHING, db_column='id_usuario')
    id_encuesta = models.ForeignKey(
        Encuesta, models.DO_NOTHING, db_column='id_encuesta')
    fecha = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'usuario_encuesta'

    def __str__(self):
        return '%s' % (self.id_usuario_encuesta)


class UsuarioRespuesta(models.Model):
    id_usuario_respuesta = models.AutoField(primary_key=True)
    id_usuario_encuesta = models.ForeignKey(
        UsuarioEncuesta, models.DO_NOTHING, db_column='id_usuario_encuesta')
    id_pregunta_respuesta = models.ForeignKey(
        PreguntaRespuesta, models.DO_NOTHING, db_column='id_pregunta_respuesta')

    class Meta:
        managed = False
        db_table = 'usuario_respuesta'

    def __str__(self):
        return '%s' % (self.id_usuario_respuesta)


class ViewPreguntaRespuesta(models.Model):
    id_survey = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=45, db_collation='utf8_general_ci')
    desc = models.TextField(
        db_collation='utf8_general_ci', blank=True, null=True)
    color = models.CharField(max_length=30, db_collation='utf8_general_ci')
    id_question = models.IntegerField()
    # Field name made lowercase.
    itemid_question = models.IntegerField(
        db_column='itemID_question', blank=True, null=True)
    question = models.TextField(db_collation='utf8_general_ci')
    answer = models.CharField(max_length=60, db_collation='utf8_general_ci')
    id_answer = models.IntegerField()
    order_answer = models.IntegerField()

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'view_pregunta_respuesta'


class ViewRespuestaEncuestas(models.Model):
    id_encuesta = models.IntegerField(primary_key=True)
    encuesta = models.CharField(max_length=45, db_collation='utf8_general_ci')
    id_usuario = models.IntegerField()
    nombre_usuario = models.CharField(
        max_length=40, db_collation='utf8_general_ci', blank=True, null=True)
    id_pregunta = models.IntegerField()
    pregunta = models.TextField(db_collation='utf8_general_ci')
    id_respuesta = models.IntegerField()
    respuesta = models.CharField(max_length=60, db_collation='utf8_general_ci')
    valor = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'view_respuesta_encuestas'
