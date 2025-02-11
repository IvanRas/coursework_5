from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Habits
from users.models import User  # импорт новой модели User

# Create your tests here.


class HabitsAPITestCase(APITestCase):
    def setUp(self):
        # Создаем тестового пользователя с использованием email
        self.user = User.objects.create_user(
            email="testuser@example.com",
            username="testusername",
            password="password",
            is_staff=True,
        )
