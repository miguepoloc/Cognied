import jwt

from datetime import datetime, timedelta
from django.db import models

from django.conf import settings

from api.models import Sexo, Estado_Civil

TIPO_DE_DOCUMENTO = [
    ("PA", 'PA'),
    ("CE", 'CÉDULA DE EXTRANJERÍA'),
    ("CC", 'CÉDULA DE CIUDADANÍA'),
    ("TI", 'TARJETA DE IDENTIDAD'),
    ("RC", 'REGISTRO CIVIL'),
]

TIPO_DE_VACUNA = [
    ("P", 'Pfizer'),
    ("M", 'Moderna'),
    ("S", 'Sinovac'),
    ("A", 'Astrazeneca'),
    ("J", 'Janssen'),
]

TIPO_DE_DISCAPACIDAD = [
    ("A", 'Auditiva'),
    ("V", 'Visual'),
    ("S", 'Sordoceguera'),
    ("I", 'Intelectual'),
    ("P", 'Psicosocial (mental)'),
    ("M", 'Múltiple'),
]


class Usuarios(models.Model):
    document = models.CharField(max_length=20, db_index=True, unique=True)
    nombre = models.CharField(max_length=200, null=False, blank=False)
    edad = models.IntegerField(null=False, blank=False)
    tipo_documento = models.CharField(
        max_length=2,
        choices=TIPO_DE_DOCUMENTO,
        default="CC",
        null=False, blank=False
    )
    sexo = models.ForeignKey(
        Sexo, on_delete=models.SET_NULL, null=True, blank=False)
    lugar_nacimiento = models.CharField(max_length=200, null=False, blank=False)
    fecha_nacimiento = models.DateTimeField(blank=False, null=False)
    estado_civil = models.ForeignKey(
        Estado_Civil, on_delete=models.SET_NULL, null=True, blank=False)
    password = models.CharField(max_length=100, blank=False, null=False)
    programa = models.CharField(max_length=200, blank=False, null=False)
    semestre = models.IntegerField(null=False, blank=False)
    covid_positivo = models.BooleanField(null=False, blank=False)
    covid_familiar = models.BooleanField(null=False, blank=False)
    covid_vacuna = models.BooleanField(null=False, blank=False)
    covid_tipo_vacuna = models.CharField(
        max_length=1,
        choices=TIPO_DE_VACUNA,
        null=True, blank=True
    )
    covid_dosis = models.BooleanField(null=True, blank=True)
    discapacidad = models.BooleanField(null=False, blank=False)
    covid_tipo_vacuna = models.CharField(
        max_length=1,
        choices=TIPO_DE_DISCAPACIDAD,
        null=True, blank=True
    )
    email = models.EmailField(
        db_index=True, unique=True, null=False, blank=False)
    telefono = models.BigIntegerField(null=False, blank=False)
    ocupacion = models.CharField(max_length=200, null=False, blank=False)

    is_controlgroup = models.BooleanField(default=True)

    is_active = models.BooleanField(default=True)

    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'document'

    def __str__(self):
        """
        Returns a string representation of this `User`.
        This string is used when a `User` is printed in the console.
        """
        return str(self.nombre + '-' + str(self.document))

    @property
    def token(self):
        """
        Allows us to get a user's token by calling `user.token` instead of
        `user.generate_jwt_token().
        The `@property` decorator above makes this possible. `token` is called
        a "dynamic property".
        """
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        """
        Generates a JSON Web Token that stores this user's ID and has an expiry
        date set to 60 days into the future.
        """
        dt = datetime.now() + timedelta(days=15)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.timestamp())
        }, settings.SECRET_KEY, algorithm='HS256')

        return token

    def _generate_jwt_token_recover(self):
        """
        Generates a JSON Web Token that stores this user's ID and has an expiry
        date set to 60 days into the future.
        """
        dt = datetime.now() + timedelta(minutes=15)
        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.timestamp())
        }, settings.SECRET_KEY, algorithm='HS256')
        return token

    def is_authenticated(self):
        return True
