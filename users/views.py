from rest_framework import generics, filters, viewsets, permissions, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from .models import Payment
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from .serializers import PaymentSerializer
from .services import (
    create_stripe_price,
    create_stripe_session,
    create_product_course,
    create_product_lesson,
)

User = get_user_model()


class PaymentList(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = {
        "paid_course": ["exact"],
        "paid_lesson": ["exact"],
        "payment_method": ["exact"],
    }
    ordering_fields = ["payment_date"]
    ordering = ["payment_date"]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ["create", "list"]:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save()


#
# class UserViewSet(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


class PaymentViewSet(CreateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        global price, product_price
        product_type = serializer.validated_data["product_type"]  # 'course' или 'lesson'
        product_id = serializer.validated_data["product_id"]  # ID курса или урока

        if product_type == "course":
            product = Course.objects.get(id=product_id)
            product_title = product.title
            product_price = product.price

            # Создаем продукт в Stripe для курса
            stripe_product = create_product_course(product_title)
            price = create_stripe_price(stripe_product.id, product_price)

            product.stripe_price_id = price.id
            product.save()

        if product_type == "lesson":
            product = Lesson.objects.get(id=product_id)
            product_title = product.title
            product_price = product.price

            # Создаем продукт в Stripe для курса
            stripe_product = create_product_lesson(product_title)
            price = create_stripe_price(stripe_product.id, product_price)

            product.stripe_price_id = price.id
            product.save()

            # Создаем сессию для оплаты
        session = create_stripe_session(price.id)

        # Сохраняем платеж в базе данных
        payment = serializer.save(
            user=self.request.user,
            amount=product_price,
            session_id=session.id,
            payment_link=session.url,
        )

        return Response(
            {
                "checkout_url": session.url,
                "payment_id": payment.id,
            },
            status=status.HTTP_201_CREATED,
        )

        # payment = serializer.save(user=self.request.user)
        # amount_in_dollar = convert_rub_to_dollars(payment.amount)
        # price = create_stripe_price(amount_in_dollar)
        # session_id, payment_link = create_stripe_session(price)
        # payment.sessions_id = session_id
        # payment.link = payment_link
        # payment.save()
