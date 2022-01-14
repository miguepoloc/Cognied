from django.contrib import admin
from .models import *


class PersonalModelAdmin(admin.ModelAdmin):
    list_display = ("nombre", "funcion", "creado")
    search_fields = ("nombre", "funcion")
    list_per_page = 10


admin.site.register(Personal, PersonalModelAdmin)
