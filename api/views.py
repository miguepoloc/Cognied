from .models import *
from .serializers import *
from rest_framework import viewsets


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