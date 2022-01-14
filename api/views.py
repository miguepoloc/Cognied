from django.shortcuts import render
from rest_framework import generics, response, status
from .models import *
from .serializers import *


class PersonalListAPIView(generics.ListAPIView):
    serializer_class = PersonalSerializer

    def get_queryset(self):
        return Personal.objects.all()


class PersonalDetailAPIView(generics.GenericAPIView):
    serializer_class = PersonalSerializer

    def get(self, request, slug):
        query_set = Personal.objects.filter(slug=slug).first()

        if query_set:
            return response.Response(self.serializer_class(query_set).data)

        return response.Response('Not found', status=status.HTTP_404_NOT_FOUND)
