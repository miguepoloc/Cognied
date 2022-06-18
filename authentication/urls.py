from django.urls import path

from .views import (
    LoginAPIView, PasswordRecover, PasswordReset, RegistrationAPIView, UserRetrieveUpdateAPIView
)

app_name = 'authentication'
urlpatterns = [
    path('list', UserRetrieveUpdateAPIView.as_view()),
    path('register', RegistrationAPIView.as_view()),
    path('login', LoginAPIView.as_view()),
    path('recover', PasswordRecover.as_view()),
    path('reset', PasswordReset.as_view())

]
