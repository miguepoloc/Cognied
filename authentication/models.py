import jwt

from datetime import datetime, timedelta
from django.db import models

from django.conf import settings

from django.db import models


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
    # Each `User` needs a human-readable unique identifier that we can use to
    # represent the `User` in the UI. We want to index this column in the
    # database to improve lookup performance.
    document = models.CharField(max_length=20, db_index=True, unique=True)
    password = models.CharField(max_length=100, blank=False, null=False)
    # We also need a way to contact the user and a way for the user to identify
    # themselves when logging in. Since we need an email address for contacting
    # the user anyways, we will also use the email for logging in because it is
    # the most common form of login credential at the time of writing.
    email = models.EmailField(db_index=True, unique=True, null=False, blank=False)
    nombre = models.CharField(max_length=200, null=False, blank=False)
    edad = models.IntegerField(null=False, blank=False)
    tipo_documento = models.CharField(
        max_length=2,
        choices=TIPO_DE_DOCUMENTO,
        default="CC",
        null=False, blank=False
    )
    sexo = models.ForeignKey(
        'api.Sexo', on_delete=models.SET_NULL, null=True, blank=False)
    departamento_nacimiento = models.CharField(
        max_length=200, null=False, blank=False)
    ciudad_nacimiento = models.CharField(
        max_length=200, null=False, blank=False)
    fecha_nacimiento = models.DateField(blank=False, null=False)
    estado_civil = models.ForeignKey(
        'api.Estado_Civil', on_delete=models.SET_NULL, null=True, blank=False)
    programa = models.CharField(max_length=200, blank=False, null=False)
    semestre = models.IntegerField(null=False, blank=False)
    covid_positivo = models.BooleanField(default=False)
    covid_familiar = models.BooleanField(default=False)
    covid_vacuna = models.BooleanField(default=False)
    covid_tipo_vacuna = models.CharField(
        max_length=1,
        choices=TIPO_DE_VACUNA,
        null=True, blank=True
    )
    covid_dosis = models.BooleanField(default=False)
    discapacidad = models.BooleanField(default=False)
    discapacidad_tipo = models.CharField(
        max_length=1,
        choices=TIPO_DE_DISCAPACIDAD,
        null=True, blank=True
    )
    telefono = models.BigIntegerField(null=False, blank=False)
    ocupacion = models.CharField(max_length=200, null=False, blank=False)

    is_controlgroup = models.BooleanField(default=True)

    is_active = models.BooleanField(default=True)

    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'document'
    # REQUIRED_FIELDS = ['document',]

    def __str__(self):
        """
        Returns a string representation of this `User`.
        This string is used when a `User` is printed in the console.
        """
        return str(self.tipo_documento + ':' + str(self.document))

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
