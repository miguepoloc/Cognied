
import pdb
from re import search
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
        userInfo.pop("is_staff", None)
        userInfo.pop("created_at", None)
        userInfo.pop("updated_at", None)

        response = {"token": usuario.token, "expiresAt": int(
            (datetime.now() + timedelta(days=15)).timestamp()), "userInfo": userInfo}

        return Response(response, status=status.HTTP_201_CREATED)


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
        userInfo.pop("is_staff", None)
        userInfo.pop("created_at", None)
        userInfo.pop("updated_at", None)

        response = {"token": data["token"], "expiresAt": int(
            (datetime.now() + timedelta(days=15)).timestamp()), "userInfo": userInfo}
        return Response(response, status=status.HTTP_200_OK)
