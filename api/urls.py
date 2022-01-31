from django.urls import include, path
from rest_framework import routers
from .views import *


router = routers.DefaultRouter()
router.register(r'personal', PersonalView, "personal")
router.register(r'usuario', UsuarioView, "usuario")
router.register(r'sexo', SexoView, "sexo")
router.register(r'estado_civil', Estado_CivilView, "estado_civil")
router.register(r'escolaridad', EscolaridadView, "escolaridad")
router.register(r'datos', DatosView, "datos")

urlpatterns = [
    path('', include(router.urls)),
]
