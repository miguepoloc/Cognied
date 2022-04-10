from django.contrib import admin
from .models import *


class PersonalModelAdmin(admin.ModelAdmin):
    list_display = ("nombre", "funcion", "creado")
    search_fields = ("nombre", "funcion")
    list_per_page = 10


admin.site.register(Personal, PersonalModelAdmin)
# admin.site.register(Usuarios)
admin.site.register(Sexo)
admin.site.register(Estado_Civil)
admin.site.register(Escolaridad)
admin.site.register(Encuesta)
admin.site.register(Pregunta)
admin.site.register(PreguntaRespuesta)
admin.site.register(Respuesta)
admin.site.register(Usuario)
admin.site.register(UsuarioEncuesta)
admin.site.register(UsuarioRespuesta)
# admin.site.register(Datos)
