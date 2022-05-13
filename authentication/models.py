import jwt

from datetime import datetime, timedelta
from django.db import models

from django.conf import settings

from django.db import models

from api.models import Sexo, Escolaridad, Estado_Civil

TIPO_DE_DOCUMENTO = [
    ("PA", 'PA'),
    ("CE", 'CE'),
    ("CC", 'CÉDULA DE CIUDADANÍA'),
    ("TI", 'TI'),
    ("RC", 'RC'),
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
    email = models.EmailField(db_index=True, unique=True)

    nombre = models.TextField(max_length=200, null=False, blank=False)
    tipo_documento = models.CharField(
        max_length=2,
        choices=TIPO_DE_DOCUMENTO,
        default="CC",
        null=True, blank=True
    )
    sexo = models.ForeignKey(
        Sexo, on_delete=models.SET_NULL, null=True, blank=True)
    lugar_nacimiento = models.TextField(max_length=200, null=True, blank=True)
    estado_civil = models.ForeignKey(
        Estado_Civil, on_delete=models.SET_NULL, null=True, blank=True)
    ocupacion = models.TextField(max_length=200, null=True, blank=True)
    escolaridad = models.ForeignKey(
        Escolaridad, on_delete=models.SET_NULL, null=True, blank=True)
    ciudad_residencia = models.TextField(max_length=200, null=True, blank=True)
    estrato = models.IntegerField(null=True, blank=True)

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

        return token.decode('utf-8')

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
        return token.decode('utf-8')
