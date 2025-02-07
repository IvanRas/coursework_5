from django.contrib.auth.models import AbstractUser
from django.db import models

from college.models import Course, Lesson


# Create your models here.


class User(AbstractUser):
    username = models.CharField(
        max_length=100,
        verbose_name="Username",
        blank=True,
        null=True,
        help_text="Введите свое имя",
    )
    email = models.EmailField(unique=True, verbose_name="Электронная почта")
    avatar = models.ImageField(
        upload_to="users/avatars",
        blank=True,
        null=True,
        verbose_name="Аватар",
        help_text="Загрузити фотографию",
    )
    phone_number = models.CharField(
        max_length=15,
        verbose_name="Номер телефона",
        help_text="Введите номер телефона",
        blank=True,
        null=True,
    )
    city = models.CharField(
        max_length=40,
        verbose_name="Город",
        blank=True,
        null=True,
        help_text="Введите город проживания",
    )

    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "Пользователи"

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class Payment(models.Model):
    PAYMENT_METHODS = [
        ("cash", "Наличными"),
        ("transfer", "Перевод на счет"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name="пользователь",
        blank=True,
        null=True,
        help_text="Введите пользователя",
    )
    payment_date = models.DateTimeField(auto_now_add=True)
    paid_course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        related_name="payments",
        null=True,
        blank=True,
        verbose_name="Оплачиваемый курс",
    )
    paid_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        related_name="payments",
        null=True,
        blank=True,
        verbose_name="Оплачиваемый урок",
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма платежа")
    session_id = models.CharField(
        max_length=255,
        verbose_name="Id сессий",
        blank=True,
        null=True,
        help_text="Введите Id сессий",
    )
    payment_link = models.URLField(max_length=400, null=True, blank=True, verbose_name="Ссылка на платеж")
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS)

    def __str__(self):
        return f"Payment of {self.amount} by {self.user.email} on {self.payment_date}"

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
