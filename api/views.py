from .models import *
from .serializers import *
from rest_framework import viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from datetime import datetime
from drf_spectacular.utils import OpenApiExample, OpenApiParameter, extend_schema, extend_schema_view, OpenApiTypes
from rest_framework.views import APIView


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
    queryset = Usuarios.objects.all()
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

        usuario_encuesta_serializer = self.get_serializer(
            data={'id_usuario': id_usuario, 'id_encuesta': id_encuesta, 'fecha': datetime.now()})
        usuario_encuesta_serializer.is_valid(raise_exception=True)
        usuario_encuesta_serializer.save()
        usuario_encuesta = usuario_encuesta_serializer.data
        data = {
            "usuario_respuestas": [],
            "errors": []
        }
        for respuesta in request.data['respuestas']:
            usuario_respuesta_serializer = UsuarioRespuestaSerializer(
                data={'id_usuario_encuesta': usuario_encuesta['id_usuario_encuesta'], 'id_pregunta_respuesta': respuesta})
            if usuario_respuesta_serializer.is_valid():
                usuario_respuesta_serializer.save()
                data["usuario_respuestas"].append(
                    usuario_respuesta_serializer.data)
            else:
                data["errors"].append(
                    {"id_respuesta": respuesta, "error": usuario_respuesta_serializer.errors})

        return Response({"usuario": usuario_encuesta, "respuestas": data})


class UsuarioRespuestaView(viewsets.ModelViewSet):
    queryset = UsuarioRespuesta.objects.all()
    serializer_class = UsuarioRespuestaSerializer



class ViewPreguntaRespuestaView(APIView): 
    permission_classes = (AllowAny,)

    def get(self, request):

        pregunta_respuesta = PreguntaRespuesta.objects.select_related('id_pregunta', 'id_respuesta', 'id_pregunta__id_encuesta').all()
        response = ViewPreguntaRespuestaSerializer(pregunta_respuesta, many=True).data
        return Response(response)


class ViewRespuestaEncuestasView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):

        respuestas_encuestas = UsuarioRespuesta.objects.select_related('id_usuario_encuesta','id_usuario_encuesta__id_usuario',
        'id_usuario_encuesta__id_encuesta', 'id_pregunta_respuesta','id_pregunta_respuesta__id_respuesta','id_pregunta_respuesta__id_pregunta', ).all()
        response = ViewRespuestaEncuestasSerializer(respuestas_encuestas, many=True).data
        return Response(response)


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


@extend_schema_view(
    list=extend_schema(parameters=[OpenApiParameter(
        "id_usuario", OpenApiTypes.NUMBER, OpenApiParameter.QUERY), ])
)
class DefinicionesUsuarioView(viewsets.ModelViewSet):
    serializer_class = DefinicionesUsuarioSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = DefinicionesUsuario.objects.all()
        id_usuario = self.request.query_params.get('id_usuario', None)
        if id_usuario is not None:
            queryset = queryset.filter(usuario=id_usuario)
        return queryset

    def create(self, request):
        # id_usuario = Usuario.objects.get(id_usuario=request.data['id_usuario'])
        respuestas = request.data['respuestas']
        response = {"definiciones": [], "errors": []}
        for respuesta in respuestas:
            # definicion = Definiciones.objects.get(id=respuesta['definicion'])
            serializer = self.serializer_class(
                data={'usuario': request.data['id_usuario'], 'definicion': respuesta['definicion'], 'definicion_usuario': respuesta['definicion_usuario']})
            try:
                serializer.is_valid(raise_exception=True)
                data = serializer.save()
                response["definiciones"].append(
                    DefinicionesUsuarioSerializer(data).data)
            except Exception as e:
                response["errors"].append(str(e))

        return Response(response)

    @action(detail=False, methods=['post'])
    def bulk_update(self, request):
        respuestas = request.data['respuestas']
        response = {"definiciones": [], "errors": []}
        for respuesta in respuestas:
            instance = DefinicionesUsuario.objects.get(
                definicion=respuesta['definicion'], usuario=request.data['id_usuario'])
            serializer = self.serializer_class(instance, data={
                                               'definicion_usuario': respuesta['definicion_usuario']}, partial=True)
            try:
                serializer.is_valid(raise_exception=True)
                serializer.save()
                response["definiciones"].append(serializer.validated_data)
            except Exception as e:
                response["errors"].append(str(e))

        return Response(response)


class AvanceModulosView(viewsets.ModelViewSet):
    queryset = AvanceModulos.objects.all()
    lookup_field = "usuario"
    serializer_class = AvanceModulosSerializer
