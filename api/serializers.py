from rest_framework import serializers
from .models import *


class PersonalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Personal
        fields = "__all__"


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
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


class DatosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Datos
        fields = "__all__"
