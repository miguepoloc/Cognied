from django.contrib import admin
from .models import *


class PersonalModelAdmin(admin.ModelAdmin):
    list_display = ("nombre", "funcion", "creado")
    search_fields = ("nombre", "funcion")
    list_per_page = 10


class PreguntaRespuestaModelAdmin(admin.ModelAdmin):
    list_display = ("id_respuesta", "id_pregunta", "id_pregunta_respuesta")
    list_per_page = 10


class UsuarioEncuestaModelAdmin(admin.ModelAdmin):
    list_display = ("id_usuario_encuesta", "id_usuario", "id_encuesta")
    list_per_page = 10


class UsuarioRespuestaModelAdmin(admin.ModelAdmin):
    list_display = ("id_usuario_respuesta",
                    "id_usuario_encuesta", "id_pregunta_respuesta")
    list_per_page = 10


class ViewPreguntaRespuestaModelAdmin(admin.ModelAdmin):
    list_display = ("id_survey", "name", "question", "answer")
    list_per_page = 10


class ViewRespuestaEncuestasModelAdmin(admin.ModelAdmin):
    list_display = ("encuesta", "nombre_usuario",
                    "pregunta", "respuesta", "valor")
    list_per_page = 10


admin.site.register(Personal, PersonalModelAdmin)
# admin.site.register(Usuarios)
admin.site.register(Sexo)
admin.site.register(Estado_Civil)
admin.site.register(Escolaridad)
admin.site.register(Encuesta)
admin.site.register(Pregunta)
admin.site.register(PreguntaRespuesta, PreguntaRespuestaModelAdmin)
admin.site.register(Respuesta)
admin.site.register(Usuario)
admin.site.register(UsuarioEncuesta, UsuarioEncuestaModelAdmin)
admin.site.register(UsuarioRespuesta, UsuarioRespuestaModelAdmin)
admin.site.register(ViewPreguntaRespuesta, ViewPreguntaRespuestaModelAdmin)
admin.site.register(ViewRespuestaEncuestas, ViewRespuestaEncuestasModelAdmin)
admin.site.register(SeccionEmocional)
admin.site.register(AvanceModulos)
# admin.site.register(Datos)
