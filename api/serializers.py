from rest_framework import serializers
from .models import *


class PersonalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Personal
        fields = "__all__"


class SexoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sexo
        fields = "__all__"


class Estado_CivilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estado_Civil
        fields = "__all__"


class EscolaridadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Escolaridad
        fields = "__all__"


class EncuestaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Encuesta
        fields = "__all__"


class PreguntaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pregunta
        fields = "__all__"

class PreguntaRespuestaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreguntaRespuesta
        fields = "__all__"

class RespuestaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Respuesta
        fields = "__all__"

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = "__all__"

class UsuarioEncuestaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioEncuesta
        fields = "__all__"

class UsuarioRespuestaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioRespuesta
        fields = "__all__"


class ViewPreguntaRespuestaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ViewPreguntaRespuesta
        fields = "__all__"

class ViewRespuestaEncuestasSerializer(serializers.ModelSerializer):
    class Meta:
        model = ViewRespuestaEncuestas
        fields = "__all__"


class SeccionEmocionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeccionEmocional
        fields = "__all__"

