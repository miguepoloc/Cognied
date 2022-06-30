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
        model = Usuarios
        fields = "__all__"


class UsuarioEncuestaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioEncuesta
        fields = "__all__"


class UsuarioRespuestaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioRespuesta
        fields = "__all__"


class ViewPreguntaRespuestaSerializer(serializers.Serializer):

    def to_representation(self, instance):
        data = {
            "id_survey": instance.id_pregunta.id_encuesta.id_encuesta,
            "name": instance.id_pregunta.id_encuesta.nombre,
            "desc": instance.id_pregunta.id_encuesta.descripcion,
            "color": instance.id_pregunta.id_encuesta.colorhex,
            "id_question": instance.id_pregunta.id_pregunta,
            "itemid_question": instance.id_pregunta.itemid,
            "question": instance.id_pregunta.pregunta,
            "answer": instance.id_respuesta.respuesta,
            "value": instance.id_respuesta.valor,
            "id_answer": instance.id_pregunta_respuesta,
            "order_answer": instance.orden
        }
        return data


class ViewRespuestaEncuestasSerializer(serializers.Serializer):

    def to_representation(self, instance):
        data = {
            "id_encuesta": instance.id_usuario_encuesta.id_encuesta.id_encuesta,
            "encuesta": instance.id_usuario_encuesta.id_encuesta.nombre,
            "id_usuario": instance.id_usuario_encuesta.id_usuario.id,
            "nombre_usuario": instance.id_usuario_encuesta.id_usuario.nombre,
            "id_pregunta": instance.id_pregunta_respuesta.id_pregunta.id_pregunta,
            "pregunta": instance.id_pregunta_respuesta.id_pregunta.pregunta,
            "id_respuesta": instance.id_pregunta_respuesta.id_respuesta.id_respuesta,
            "respuesta": instance.id_pregunta_respuesta.id_respuesta.respuesta,
            "valor": instance.id_pregunta_respuesta.id_respuesta.valor}
        return data


class ViewUsuarioRespuestaSerializer(serializers.Serializer):

    def to_representation(self, instance):
        data = {
            "id_encuesta": instance.id_usuario_encuesta.id_encuesta.id_encuesta,
            "fecha": instance.id_usuario_encuesta.fecha,
        }
        return data


class EmocionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emocion
        fields = "__all__"


class ClasificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clasificacion
        fields = "__all__"


class EmocionListSerializer(serializers.ModelSerializer):
    clasificacion = ClasificacionSerializer(many=True, read_only=True)

    class Meta:
        model = Emocion
        fields = "__all__"


class DefinicionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Definiciones
        fields = "__all__"


class DefinicionesUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = DefinicionesUsuario
        fields = "__all__"

    def create(self, validated_data):
        if DefinicionesUsuario.objects.filter(definicion=validated_data['definicion'], usuario=validated_data['usuario']).exists():
            raise serializers.ValidationError(
                "Ya existe una definicion para este usuario")
        return super().create(validated_data)


class AvanceModulosSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvanceModulos
        fields = "__all__"
