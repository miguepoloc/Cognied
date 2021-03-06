from django.urls import include, path
from rest_framework import routers
from .views import *


router = routers.DefaultRouter()
router.register(r'personal', PersonalView, "personal")
router.register(r'sexo', SexoView, "sexo")
router.register(r'estado_civil', Estado_CivilView, "estado_civil")
router.register(r'escolaridad', EscolaridadView, "escolaridad")
router.register(r'encuesta', EncuestaView, "encuesta")
router.register(r'pregunta', PreguntaView, "pregunta")
router.register(r'pregunta_respuesta',
                PreguntaRespuestaView, "pregunta_respuesta")
router.register(r'respuesta', RespuestaView, "respuesta")
router.register(r'usuario', UsuarioView, "usuario")
router.register(r'usuario_encuesta', UsuarioEncuestaView, "usuario_encuesta")
router.register(r'usuario_respuesta',
                UsuarioRespuestaView, "usuario_respuesta")
router.register(r'emocion', EmocionView, 'emocion_view')
router.register(r'clasificacion', ClasificacionView, 'clasificacion_view')
router.register(r'definiciones', DefinicionesView, 'definiciones_view')
router.register(r'definiciones_usuario',
                DefinicionesUsuarioView, 'definiciones_usuario_view')
router.register(r'avance_modulos', AvanceModulosView, 'avance_modulos')
router.register(r'programa_academico', ProgramaAcademicoView, 'programa_academico')


urlpatterns = [
    path('', include(router.urls)),
    path('vista_pregunta_respuesta', ViewPreguntaRespuestaView.as_view()),
    path('vista_respuesta_encuestas', ViewRespuestaEncuestasView.as_view()),
    path('vista_usuario_respuestas', ViewUsuarioRespuestaView.as_view())
]
