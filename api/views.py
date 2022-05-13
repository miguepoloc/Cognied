from .models import *
from .serializers import *
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


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


class UsuarioEncuestaView(viewsets.ModelViewSet):
    queryset = UsuarioEncuesta.objects.all()
    serializer_class = UsuarioEncuestaSerializer

    def create(self, request):
        id_usuario = request.data['id_usuario'],
        id_encuesta = request.data['id_encuesta'],

        usuario_encuesta = self.get_serializer(data={'id_usuario': id_usuario, 'id_encuesta': id_encuesta, 'fecha': datetime.now()})
        usuario_encuesta.is_valid(raise_exception=True)
        usuario_encuesta.save()
        usuario_encuesta = usuario_encuesta.data
        usuario_respuestas = UsuarioRespuestaSerializer(data=[{'id_usuario_encuesta': usuario_encuesta['id'], 'id_pregunta_respuesta':x['id']} for x in request.data["respuestas"]], many=True)
        usuario_respuestas.is_valid(raise_exception=True)
        usuario_respuestas.save()
        return Response({usuario_encuesta.data, usuario_respuestas.data})


class UsuarioRespuestaView(viewsets.ModelViewSet):
    queryset = UsuarioRespuesta.objects.all()
    serializer_class = UsuarioRespuestaSerializer


class ViewPreguntaRespuestaView(viewsets.ModelViewSet):
    queryset = ViewPreguntaRespuesta.objects.all().values()
    serializer_class = ViewPreguntaRespuestaSerializer


class ViewRespuestaEncuestasView(viewsets.ModelViewSet):
    queryset = ViewRespuestaEncuestas.objects.all()
    serializer_class = ViewRespuestaEncuestasSerializer


class SeccionEmocionalView(viewsets.ModelViewSet):
    queryset = SeccionEmocional.objects.all()
    serializer_class = SeccionEmocionalSerializer
