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
router.register(r'pregunta_respuesta', PreguntaRespuestaView, "pregunta_respuesta")
router.register(r'respuesta', RespuestaView, "respuesta")
router.register(r'usuario', UsuarioView, "usuario")
router.register(r'usuario_encuesta', UsuarioEncuestaView, "usuario_encuesta")
router.register(r'usuario_respuesta', UsuarioRespuestaView, "usuario_respuesta")
router.register(r'vista_pregunta_respuesta', ViewPreguntaRespuestaView, "vista_pregunta_respuesta")
router.register(r'vista_respuesta_encuestas', ViewRespuestaEncuestasView, "vista_respuesta_encuestas")
router.register(r'seccion_emocional', SeccionEmocionalView, "seccion_emocional")


urlpatterns = [
    path('', include(router.urls)),
]
