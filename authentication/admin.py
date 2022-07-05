from django.contrib import admin
from .models import *


class UsuariosModelAdmin(admin.ModelAdmin):
    list_display = ("document", "nombre", "sexo", "email",
                    "is_controlgroup", "is_staff")
    list_per_page = 100


admin.site.register(Usuarios, UsuariosModelAdmin)
