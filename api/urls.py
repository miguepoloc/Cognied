from django.urls import path
from .views import *

urlpatterns = [
    path("personal", PersonalListAPIView.as_view(), name="personals"),
    path("personal/<str:slug>", PersonalDetailAPIView.as_view(), name="personal"),
]
