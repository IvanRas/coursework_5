from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.apps import UsersConfig
from rest_framework.permissions import AllowAny

from users.views import UserRegisterView

# Описание маршрутизации для User

app_name = UsersConfig.name


urlpatterns = [
    path(
        "register/", UserRegisterView.as_view(), name="user-register"
    ),  # Регистрация пользователя
    path(
        "token/", TokenObtainPairView.as_view(), name="login"
    ),  # Авторизация пользователя
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

