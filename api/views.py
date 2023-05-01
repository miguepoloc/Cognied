from django.db.models import Case, FloatField, Sum, Value, When
from django.db.models.functions import ExtractYear
from drf_spectacular.utils import (OpenApiParameter, OpenApiTypes,
                                   extend_schema, extend_schema_view)
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (AvanceModulos, Clasificacion, Definiciones,
                     DefinicionesUsuario, Emocion, Encuesta, Escolaridad,
                     Estado_Civil, Personal, Pregunta, PreguntaRespuesta,
                     ProgramaAcademico, Respuesta, Sexo, UsuarioEncuesta,
                     UsuarioRespuesta, Usuarios)
from .serializers import (AvanceModulosSerializer, ClasificacionSerializer,
                          DefinicionesSerializer,
                          DefinicionesUsuarioSerializer, EmocionListSerializer,
                          EmocionSerializer, EncuestaSerializer,
                          EscolaridadSerializer, Estado_CivilSerializer,
                          PersonalSerializer, PreguntaRespuestaSerializer,
                          PreguntaSerializer, ProgramaAcademicoSerializer,
                          RespuestaSerializer, SexoSerializer,
                          UsuarioEncuestaSerializer,
                          UsuarioRespuestaSerializer, UsuarioSerializer,
                          ViewPreguntaRespuestaSerializer,
                          ViewRespuestaEncuestasSerializer)
from .utils.processdata import processdata


class PersonalView(viewsets.ModelViewSet):
    """ViewSet for viewing and editing Personal objects"""

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
            data={'id_usuario': id_usuario, 'id_encuesta': id_encuesta, 'fecha': fecha}
        )
        usuario_encuesta_serializer.is_valid(raise_exception=True)
        usuario_encuesta_serializer.save()
        usuario_encuesta = usuario_encuesta_serializer.data
        data = {"usuario_respuestas": [], "errors": []}
        for respuesta in request.data['respuestas']:
            usuario_respuesta_serializer = UsuarioRespuestaSerializer(
                data={
                    'id_usuario_encuesta': usuario_encuesta['id_usuario_encuesta'],
                    'id_pregunta_respuesta': respuesta,
                }
            )
            if usuario_respuesta_serializer.is_valid():
                usuario_respuesta_serializer.save()
                data["usuario_respuestas"].append(usuario_respuesta_serializer.data)
            else:
                data["errors"].append({"id_respuesta": respuesta, "error": usuario_respuesta_serializer.errors})

        return Response({"usuario": usuario_encuesta, "respuestas": data})


class UsuarioRespuestaView(viewsets.ModelViewSet):
    queryset = UsuarioRespuesta.objects.all()
    serializer_class = UsuarioRespuestaSerializer


class ViewPreguntaRespuestaView(APIView):
    def get(self, request):
        pregunta_respuesta = PreguntaRespuesta.objects.select_related(
            'id_pregunta', 'id_respuesta', 'id_pregunta__id_encuesta'
        ).all()
        response = ViewPreguntaRespuestaSerializer(pregunta_respuesta, many=True).data
        return Response(response)


class ViewRespuestaEncuestasView(APIView):
    def get(self, request):
        respuestas_encuestas = UsuarioRespuesta.objects.select_related(
            'id_usuario_encuesta',
            'id_usuario_encuesta__id_usuario',
            'id_usuario_encuesta__id_encuesta',
            'id_pregunta_respuesta',
            'id_pregunta_respuesta__id_respuesta',
            'id_pregunta_respuesta__id_pregunta',
        ).all()
        response = ViewRespuestaEncuestasSerializer(respuestas_encuestas, many=True).data
        return Response(response)


class ViewUsuarioRespuestaView(APIView):
    def get(self, request):
        user = request.user
        u_e = UsuarioEncuesta.objects.filter(id_usuario=user).select_related(
            "id_encuesta", "usuariorespuesta", "usuariorespuesta__id_pregunta_respuesta"
        )
        u_en = u_e.values("fecha", "id_encuesta", "usuariorespuesta__id_pregunta_respuesta")
        data = []
        u_fechas = u_e.order_by("fecha").values("fecha").distinct()
        for u_fecha in u_fechas:
            buffer = {"fecha": str(u_fecha["fecha"]), "respuestas": []}
            u_encuestas = u_e.filter(fecha=u_fecha["fecha"]).order_by("id_encuesta").values("id_encuesta").distinct()
            for u_encuesta in u_encuestas:
                buffer["respuestas"].append(
                    {
                        "id_encuesta": u_encuesta["id_encuesta"],
                        "respuestas": u_en.filter(
                            id_encuesta=u_encuesta["id_encuesta"], fecha=u_fecha["fecha"]
                        ).values_list('usuariorespuesta__id_pregunta_respuesta', flat=True),
                    }
                )
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


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter("id_usuario", OpenApiTypes.NUMBER, OpenApiParameter.QUERY),
        ]
    )
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
                data={
                    'usuario': request.data['id_usuario'],
                    'definicion': respuesta['definicion'],
                    'definicion_usuario': respuesta['definicion_usuario'],
                }
            )
            try:
                serializer.is_valid(raise_exception=True)
                data = serializer.save()
                response["definiciones"].append(DefinicionesUsuarioSerializer(data).data)
            except Exception as e:
                response["errors"].append(str(e))

        return Response(response)

    @action(detail=False, methods=['post'])
    def bulk_update(self, request):
        respuestas = request.data['respuestas']
        response = {"definiciones": [], "errors": []}
        for respuesta in respuestas:
            instance = DefinicionesUsuario.objects.get(
                definicion=respuesta['definicion'], usuario=request.data['id_usuario']
            )
            serializer = self.serializer_class(
                instance, data={'definicion_usuario': respuesta['definicion_usuario']}, partial=True
            )
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
        avance_autoevaluativo = 3
        users = AvanceModulos.objects.filter(autoevaluativo=avance_autoevaluativo).values("usuario").distinct()
        subquery = UsuarioRespuesta.objects.filter(id_usuario_encuesta__id_usuario__in=users).order_by(
            "id_usuario_encuesta__id_usuario__id", 'id_usuario_encuesta'
        )
        subquery = subquery.values(
            "id_usuario_encuesta__id_usuario__id",
            "id_usuario_encuesta__id_usuario__tipo_documento",
            "id_usuario_encuesta__id_usuario__sexo__sexo",
            "id_usuario_encuesta__id_usuario__departamento_nacimiento",
            "id_usuario_encuesta__id_usuario__ciudad_nacimiento",
            "id_usuario_encuesta__id_usuario__fecha_nacimiento",
            "id_usuario_encuesta__id_usuario__estado_civil__estado_civil",
            "id_usuario_encuesta__id_usuario__programa_academico__facultad",
            "id_usuario_encuesta__id_usuario__programa_academico__programa",
            "id_usuario_encuesta__id_usuario__semestre",
            "id_usuario_encuesta__id_usuario__covid_positivo",
            "id_usuario_encuesta__id_usuario__covid_familiar",
            "id_usuario_encuesta__id_usuario__covid_vacuna",
            "id_usuario_encuesta__id_usuario__covid_tipo_vacuna",
            "id_usuario_encuesta__id_usuario__covid_dosis",
            "id_usuario_encuesta__id_usuario__discapacidad",
            "id_usuario_encuesta__id_usuario__discapacidad_tipo",
            "id_usuario_encuesta__id_usuario__ocupacion",
            "id_usuario_encuesta__id_usuario__is_controlgroup",
            "id_usuario_encuesta__id_usuario__is_active",
            "id_usuario_encuesta__id_usuario__is_staff",
            "id_usuario_encuesta__id_encuesta__id_encuesta",
            "id_usuario_encuesta__id_encuesta__nombre",
            "id_usuario_encuesta__fecha",
            "id_usuario_encuesta__id_usuario_encuesta",
            "id_pregunta_respuesta__id_pregunta__id_pregunta",
            "id_pregunta_respuesta__id_pregunta__pregunta",
            "id_pregunta_respuesta__id_pregunta__itemid",
            "id_pregunta_respuesta__id_respuesta__valor",
            "id_pregunta_respuesta__id_respuesta__respuesta",
        ).annotate(
            edad=2022 - ExtractYear('id_usuario_encuesta__id_usuario__fecha_nacimiento'),
        )

        detalle = processdata(list(subquery))

        return Response(detalle)


class EncuestaDetallex(APIView):
    def get(self, request):
        avance_autoevaluativo = 3
        users = AvanceModulos.objects.filter(autoevaluativo=avance_autoevaluativo).values("usuario").distinct()
        subquery = UsuarioRespuesta.objects.filter(id_usuario_encuesta__id_usuario__in=users).order_by(
            "id_usuario_encuesta__id_usuario__id", 'id_usuario_encuesta'
        )
        subquery = subquery.values(
            "id_usuario_encuesta__id_usuario__id",
            "id_usuario_encuesta__id_usuario__tipo_documento",
            "id_usuario_encuesta__id_usuario__sexo__sexo",
            "id_usuario_encuesta__id_usuario__departamento_nacimiento",
            "id_usuario_encuesta__id_usuario__ciudad_nacimiento",
            "id_usuario_encuesta__id_usuario__fecha_nacimiento",
            "id_usuario_encuesta__id_usuario__estado_civil__estado_civil",
            "id_usuario_encuesta__id_usuario__programa_academico__facultad",
            "id_usuario_encuesta__id_usuario__programa_academico__programa",
            "id_usuario_encuesta__id_usuario__semestre",
            "id_usuario_encuesta__id_usuario__covid_positivo",
            "id_usuario_encuesta__id_usuario__covid_familiar",
            "id_usuario_encuesta__id_usuario__covid_vacuna",
            "id_usuario_encuesta__id_usuario__covid_tipo_vacuna",
            "id_usuario_encuesta__id_usuario__covid_dosis",
            "id_usuario_encuesta__id_usuario__discapacidad",
            "id_usuario_encuesta__id_usuario__discapacidad_tipo",
            "id_usuario_encuesta__id_usuario__ocupacion",
            "id_usuario_encuesta__id_usuario__is_controlgroup",
            "id_usuario_encuesta__id_usuario__is_active",
            "id_usuario_encuesta__id_usuario__is_staff",
            "id_usuario_encuesta__id_encuesta__id_encuesta",
            "id_usuario_encuesta__id_encuesta__nombre",
            "id_usuario_encuesta__fecha",
            "id_usuario_encuesta__id_usuario_encuesta",
            "id_pregunta_respuesta__id_pregunta__id_pregunta",
            "id_pregunta_respuesta__id_pregunta__pregunta",
            "id_pregunta_respuesta__id_pregunta__itemid",
            "id_pregunta_respuesta__id_respuesta__valor",
            "id_pregunta_respuesta__id_respuesta__respuesta",
        ).annotate(
            edad=2022 - ExtractYear('id_usuario_encuesta__id_usuario__fecha_nacimiento'),
        )
        subquery = subquery

        subquery2 = UsuarioRespuesta.objects.filter(id_usuario_encuesta__id_usuario__in=users)
        subquery2 = subquery2.values(
            'id_usuario_encuesta__id_encuesta',
            "id_usuario_encuesta__id_usuario_encuesta",
            "id_usuario_encuesta__id_usuario",
        )
        subquery2 = subquery2.annotate(
            resultado=Case(
                When(id_usuario_encuesta__id_encuesta=3, then=Sum("id_pregunta_respuesta__id_respuesta__valor")),
                When(id_usuario_encuesta__id_encuesta=4, then=Sum("id_pregunta_respuesta__id_respuesta__valor")),
                default=Value(0),
                output_field=FloatField(),
            )
        )
        subquery2 = subquery2.order_by(
            "id_usuario_encuesta__id_usuario", "id_usuario_encuesta__id_usuario_encuesta"
        ).values(
            'id_usuario_encuesta__id_encuesta',
            'id_usuario_encuesta__id_encuesta__nombre',
            "id_usuario_encuesta__id_usuario_encuesta",
            "id_usuario_encuesta__id_usuario",
            "id_usuario_encuesta__id_usuario__nombre",
            "resultado",
        )
        subquery2 = subquery2

        return Response(subquery)


class UsuarioDetalle(APIView):
    def get(self, request):
        users = (
            Usuarios.objects.values(
                "id",
                "tipo_documento",
                "sexo__sexo",
                "departamento_nacimiento",
                "ciudad_nacimiento",
                "fecha_nacimiento",
                "estado_civil__estado_civil",
                "programa_academico__facultad",
                "programa_academico__programa",
                "semestre",
                "covid_positivo",
                "covid_familiar",
                "covid_vacuna",
                "covid_tipo_vacuna",
                "covid_dosis",
                "discapacidad",
                "discapacidad_tipo",
                "ocupacion",
                "is_controlgroup",
                "is_active",
                "is_staff",
            )
            .annotate(
                edad=2022 - ExtractYear('fecha_nacimiento'),
            )
            .order_by("id")
        )

        return Response(users)
