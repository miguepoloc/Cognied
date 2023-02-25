from .models import *
from .serializers import *
from rest_framework import viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from datetime import datetime
from drf_spectacular.utils import OpenApiExample, OpenApiParameter, extend_schema, extend_schema_view, OpenApiTypes
from rest_framework.views import APIView
from django.db.models import Subquery, OuterRef
from django.db.models import FloatField, Case, Value, When, Sum, Avg


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


class UsuarioEncuestaView(viewsets.ModelViewSet):
    queryset = UsuarioEncuesta.objects.all()
    serializer_class = UsuarioEncuestaSerializer

    def create(self, request):
        id_usuario = request.data['id_usuario']
        id_encuesta = request.data['id_encuesta']
        fecha = request.data['fecha']
        usuario_encuesta_serializer = self.get_serializer(
            data={'id_usuario': id_usuario, 'id_encuesta': id_encuesta, 'fecha': fecha})
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

    def get(self, request):

        pregunta_respuesta = PreguntaRespuesta.objects.select_related(
            'id_pregunta', 'id_respuesta', 'id_pregunta__id_encuesta').all()
        response = ViewPreguntaRespuestaSerializer(
            pregunta_respuesta, many=True).data
        return Response(response)


class ViewRespuestaEncuestasView(APIView):

    def get(self, request):

        respuestas_encuestas = UsuarioRespuesta.objects.select_related('id_usuario_encuesta', 'id_usuario_encuesta__id_usuario',
                                                                       'id_usuario_encuesta__id_encuesta', 'id_pregunta_respuesta', 'id_pregunta_respuesta__id_respuesta', 'id_pregunta_respuesta__id_pregunta', ).all()
        response = ViewRespuestaEncuestasSerializer(
            respuestas_encuestas, many=True).data
        return Response(response)


class ViewUsuarioRespuestaView(APIView):

    def get(self, request):
        user = request.user
        u_e = UsuarioEncuesta.objects.filter(id_usuario=user).select_related(
            "id_encuesta", "usuariorespuesta", "usuariorespuesta__id_pregunta_respuesta")
        u_en = u_e.values("fecha", "id_encuesta",
                          "usuariorespuesta__id_pregunta_respuesta")
        data = []
        u_fechas = u_e.order_by("fecha").values("fecha").distinct()
        for u_fecha in u_fechas:
            buffer = {"fecha": str(u_fecha["fecha"]), "respuestas": []}
            u_encuestas = u_e.filter(fecha=u_fecha["fecha"]).order_by(
                "id_encuesta").values("id_encuesta").distinct()
            for u_encuesta in u_encuestas:
                buffer["respuestas"].append({"id_encuesta": u_encuesta["id_encuesta"], "respuestas": u_en.filter(
                    id_encuesta=u_encuesta["id_encuesta"], fecha=u_fecha["fecha"]).values_list('usuariorespuesta__id_pregunta_respuesta', flat=True)})
            data.append(buffer)
        return Response(data)


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


@ extend_schema_view(
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

    @ action(detail=False, methods=['post'])
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


class ProgramaAcademicoView(viewsets.ModelViewSet):
    queryset = ProgramaAcademico.objects.all()
    serializer_class = ProgramaAcademicoSerializer


class EncuestaDetalle(APIView):
    def get(self, request):
        encuesta_id = 4
        avance_autoevaluativo = 3
        # subquery = UsuarioEncuesta.objects.filter(id_usuario=OuterRef(
        #     'id_usuario_encuesta')).order_by('id_usuario_encuesta')[:1]
        users = AvanceModulos.objects.filter(
            autoevaluativo=avance_autoevaluativo).values("usuario").distinct()
        subquery = UsuarioRespuesta.objects.filter(
            id_usuario_encuesta__id_usuario__in=users).order_by('id_usuario_encuesta')
        subquery = subquery.values("id_usuario_encuesta__id_usuario__id", "id_usuario_encuesta__id_usuario__nombre", "id_usuario_encuesta__id_encuesta__id_encuesta", "id_usuario_encuesta__id_encuesta__nombre", "id_usuario_encuesta__fecha", "id_usuario_encuesta__id_usuario_encuesta",
                                   "id_pregunta_respuesta__id_pregunta__id_pregunta", "id_pregunta_respuesta__id_pregunta__pregunta", "id_pregunta_respuesta__id_pregunta__itemid", "id_pregunta_respuesta__id_respuesta__valor", "id_pregunta_respuesta__id_respuesta__respuesta")
        
        subquery2 = UsuarioRespuesta.objects.filter(
            id_usuario_encuesta__id_usuario__in=users)
        subquery2 = subquery2.values('id_usuario_encuesta__id_encuesta',
                                     "id_usuario_encuesta__id_usuario_encuesta", "id_usuario_encuesta__id_usuario")
        subquery2 = subquery2.annotate(resultado=Case(
            When(id_usuario_encuesta__id_encuesta=3,
                 then=Sum("id_pregunta_respuesta__id_respuesta__valor")),
            When(id_usuario_encuesta__id_encuesta=4,
                 then=Avg("id_pregunta_respuesta__id_respuesta__valor")),
            default=Value(0),
            output_field=FloatField()
        ))
        subquery2 = subquery2.order_by('id_usuario_encuesta__id_encuesta', "id_usuario_encuesta__id_usuario_encuesta", "id_usuario_encuesta__id_usuario").values(
            'id_usuario_encuesta__id_encuesta', "id_usuario_encuesta__id_usuario_encuesta", "id_usuario_encuesta__id_usuario", "resultado")
        print(subquery.query)
        return Response({"data1": subquery, "data2": subquery2})
