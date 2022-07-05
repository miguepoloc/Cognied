
from django.core.mail import send_mail
from .models import Usuarios
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers

from rest_framework.decorators import api_view, permission_classes

from rest_framework import viewsets, exceptions, parsers, renderers, status
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from datetime import datetime, timedelta
from drf_spectacular.utils import OpenApiExample, OpenApiParameter, extend_schema, extend_schema_view, inline_serializer

from .renderers import UserJSONRenderer
from .serializers import (
    LoginSerializer, RegistrationSerializer, UserSerializer,
)
from .models import *

from django.contrib.auth import hashers


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    # permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        # There is nothing to validate or save here. Instead, we just want the
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer_data = request.data

        # Here is that serialize, validate, save pattern we talked about
        # before.
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


@permission_classes([AllowAny])
class RegistrationAPIView(APIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        # The create serializer, validate serializer, save serializer pattern
        # below is common and you will see it a lot throughout this course and
        # your own work later on. Get familiar with it.
        serializer = self.serializer_class(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        usuario = serializer.save()
        userInfo = UserSerializer(usuario, partial=True).data
        userInfo.pop("is_active", None)
        # userInfo.pop("is_staff", None)
        userInfo.pop("created_at", None)
        userInfo.pop("updated_at", None)

        response = {"token": usuario.token, "expiresAt": int(
            (datetime.now() + timedelta(days=15)).timestamp()), "userInfo": userInfo}

        return Response(response, status=status.HTTP_201_CREATED)


@permission_classes([AllowAny])
class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    @extend_schema(
        examples=[
            OpenApiExample(
                'Ejemplo 1',
                summary='Modelo de prueba',
                value={
                        "document": "1234567",
                                    "password": "admin123",

                },
                request_only=True,  # signal that example only applies to requests
                response_only=False,  # signal that example only applies to responses
            ),
        ],
    )
    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        data = serializer.validate(user)
        userInfo = UserSerializer(data["user"]).data
        userInfo.pop("is_active", None)
        # userInfo.pop("is_staff", None)
        userInfo.pop("created_at", None)
        userInfo.pop("updated_at", None)

        response = {"token": data["token"], "expiresAt": int(
            (datetime.now() + timedelta(days=15)).timestamp()), "userInfo": userInfo}
        return Response(response, status=status.HTTP_200_OK)


class PasswordRecover(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)

    def post(self, request):
        email = request.data["email"]
        user = Usuarios.objects.filter(email=email)

        if user.exists():
            user = user.first()
            recover_url = "https://digitalmenteunimagdalena.com/reset?token=" + \
                str(user.token)
            token = user.token
            send_mail(
                subject='Recuperación de contraseña',
                message='Hola ' + user.nombre + '\n\n' + 'Para recuperar tu contraseña, ingresa al siguiente enlace: ' +
                recover_url + '\n\n' + 'Este enlace expirará en 15 días.',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
            )
            return (Response({"message": "Se ha enviado un correo a " + user.email + " con instrucciones para recuperar la contraseña."}, status=status.HTTP_200_OK))
        return (Response({"message": "El correo no existe en la base de datos."}, status=status.HTTP_400_BAD_REQUEST))


class PasswordReset(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)

    def post(self, request):
        token = request.data["token"]
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user = Usuarios.objects.get(pk=payload['id'])
        if request.data["password"] and user:
            user.password = hashers.make_password(request.data["password"])
            user.save()
            userInfo = UserSerializer(user).data
            userInfo.pop("is_active", None)
            # userInfo.pop("is_staff", None)
            userInfo.pop("created_at", None)
            userInfo.pop("updated_at", None)

            response = {"message": "Contraseña actualizada correctamente", "token": user.token, "expiresAt": int(
                (datetime.now() + timedelta(days=15)).timestamp()), "userInfo": userInfo}
            return Response(response, status=status.HTTP_200_OK)
        return (Response({"message": "No se ha recibido ninguna contraseña."}, status=status.HTTP_400_BAD_REQUEST))
