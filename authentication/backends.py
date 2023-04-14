import jwt
from django.conf import settings
from drf_spectacular.extensions import OpenApiAuthenticationExtension
from rest_framework import authentication, exceptions

from .models import Usuarios


class JWTAuthentication(authentication.BaseAuthentication):
    authentication_header_prefix = 'Bearer'

    def authenticate(self, request):
        request.user = None

        auth_header = authentication.get_authorization_header(request).split()
        auth_header_prefix = self.authentication_header_prefix.lower()

        if not auth_header:
            return None

        if len(auth_header) == 1:
            return None

        elif len(auth_header) > 2:
            return None

        prefix = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8')

        if prefix.lower() != auth_header_prefix:
            return None
        return self._authenticate_credentials(request, token)

    def _authenticate_credentials(self, request, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except Exception:
            msg = 'Token Invalido'
            raise exceptions.AuthenticationFailed(msg)

        try:
            user = Usuarios.objects.get(pk=payload['id'])
        except Usuarios.DoesNotExist:
            msg = 'Usuario No encontrado '
            raise exceptions.AuthenticationFailed(msg)

        if not user.is_active:
            msg = 'Usuario No Activo'
            raise exceptions.AuthenticationFailed(msg)

        return (user, token)


class JWTAuthenticationExt(OpenApiAuthenticationExtension):
    target_class = 'authentication.backends.JWTAuthentication'  # full import path OR class ref
    name = 'JWTAuthentication'  # name used in the schema
    match_subclasses = True
    priority = 1

    def get_security_definition(self, auto_schema):
        return {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': 'Token-based authentication with required prefix "%s"'
            % self.target.authentication_header_prefix,
        }
