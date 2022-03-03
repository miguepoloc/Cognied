from django.urls import path

from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView
)

app_name = 'authentication'
urlpatterns = [
    path('list', UserRetrieveUpdateAPIView.as_view()),
    path('register', RegistrationAPIView.as_view()),
    path('login', LoginAPIView.as_view()),
]
