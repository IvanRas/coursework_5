from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.apps import UsersConfig
from users.views import PaymentList, PaymentViewSet
from rest_framework.permissions import AllowAny


# Описание маршрутизации для User

app_name = UsersConfig.name

urlpatterns = [
    path("payments/", PaymentList.as_view(), name="payment-list"),
    # path("person/", UserViewSet.as_view(), name="person"),
    path(
        "login/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="login",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
    path("create-payment/", PaymentViewSet.as_view(), name="create_payment"),
]
