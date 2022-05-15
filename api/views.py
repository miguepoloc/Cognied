from os import device_encoding
from .models import *
from .serializers import *
from rest_framework import viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from datetime import datetime


class PersonalView(viewsets.ModelViewSet):
    queryset = Personal.objects.all().order_by('id')
    serializer_class = PersonalSerializer


class SexoView(viewsets.ModelViewSet):
    queryset = Sexo.objects.all().order_by('id')
    serializer_class = SexoSerializer


class Estado_CivilView(viewsets.ModelViewSet):
    queryset = Estado_Civil.objects.all().order_by('id')
    serializer_class = Estado_CivilSerializer


class EscolaridadView(viewsets.ModelViewSet):
    queryset = Escolaridad.objects.all().order_by('id')
    serializer_class = EscolaridadSerializer


class EncuestaView(viewsets.ModelViewSet):
    queryset = Encuesta.objects.all()
    serializer_class = EncuestaSerializer


class PreguntaView(viewsets.ModelViewSet):
    queryset = Pregunta.objects.all()
    serializer_class = PreguntaSerializer


class PreguntaRespuestaView(viewsets.ModelViewSet):
    queryset = PreguntaRespuesta.objects.all()
    serializer_class = PreguntaRespuestaSerializer


class RespuestaView(viewsets.ModelViewSet):
    queryset = Respuesta.objects.all()
    serializer_class = RespuestaSerializer


class UsuarioView(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer


@permission_classes([AllowAny])
class UsuarioEncuestaView(viewsets.ModelViewSet):
    queryset = UsuarioEncuesta.objects.all()
    serializer_class = UsuarioEncuestaSerializer

    # {
    #     "id_usuario": 1,
    #     "id_encuesta": 1,
    #     "respuestas": [
    #         1,
    #         2,
    #         3,
    #         4,
    #     ]

    # }
    def create(self, request):
        id_usuario = request.data['id_usuario']
        id_encuesta = request.data['id_encuesta']

        usuario_encuesta_serializer = self.get_serializer(data={'id_usuario': id_usuario, 'id_encuesta': id_encuesta, 'fecha': datetime.now()})
        usuario_encuesta_serializer.is_valid(raise_exception=True)
        usuario_encuesta_serializer.save()
        usuario_encuesta = usuario_encuesta_serializer.data
        data = {
            "usuario_respuestas": [],
            "errors": []
        }
        for respuesta in request.data['respuestas']:
            usuario_respuesta_serializer = UsuarioRespuestaSerializer(data={'id_usuario_encuesta': usuario_encuesta['id_usuario_encuesta'], 'id_pregunta_respuesta': respuesta})
            if usuario_respuesta_serializer.is_valid():
                usuario_respuesta_serializer.save()
                data["usuario_respuestas"].append(usuario_respuesta_serializer.data)
            else:
                data["errors"].append({"id_respuesta": respuesta, "error": usuario_respuesta_serializer.errors})

        return Response({"usuario": usuario_encuesta, "respuestas": data})


class UsuarioRespuestaView(viewsets.ModelViewSet):
    queryset = UsuarioRespuesta.objects.all()
    serializer_class = UsuarioRespuestaSerializer


@permission_classes([AllowAny])
class ViewPreguntaRespuestaView(viewsets.ModelViewSet):
    queryset = ViewPreguntaRespuesta.objects.all().values()
    serializer_class = ViewPreguntaRespuestaSerializer


class ViewRespuestaEncuestasView(viewsets.ModelViewSet):
    queryset = ViewRespuestaEncuestas.objects.all()
    serializer_class = ViewRespuestaEncuestasSerializer


class SeccionEmocionalView(viewsets.ModelViewSet):
    queryset = SeccionEmocional.objects.all()
    serializer_class = SeccionEmocionalSerializer


class EmocionView(viewsets.ModelViewSet):
    queryset = Emocion.objects.all()
    serializer_class = EmocionSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return EmocionListSerializer
        else:
            return EmocionSerializer


class ClasificacionView(viewsets.ModelViewSet):
    queryset = Clasificacion.objects.all()
    serializer_class = ClasificacionSerializer


class DefinicionesView(viewsets.ModelViewSet):
    queryset = Definiciones.objects.all()
    serializer_class = DefinicionesSerializer


class DefinicionesUsuarioView(viewsets.ModelViewSet):
    queryset = DefinicionesUsuario.objects.all()
    serializer_class = DefinicionesUsuarioSerializer

    def create(self, request):
        # id_usuario = Usuario.objects.get(id_usuario=request.data['id_usuario'])
        respuestas = request.data['respuestas']
        response = {"definiciones": [], "errors": []}
        for respuesta in respuestas:
            # definicion = Definiciones.objects.get(id=respuesta['definicion'])
            serializer = self.serializer_class(data={'usuario': request.data['id_usuario'], 'definicion': respuesta['definicion'], 'definicion_usuario': respuesta['definicion_usuario']})
            try:
                serializer.is_valid(raise_exception=True)
                serializer.save()
                response["definiciones"].append(serializer.data)
            except Exception as e:
                response["errors"].append(str(e))

        return Response(response)
