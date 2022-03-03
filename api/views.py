from .models import *
from .serializers import *
from .utils import *
from rest_framework.permissions import IsAuthenticated, AllowAny

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
