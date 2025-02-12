from django.db import models

from config import settings


# Create your models here.


class Habits(models.Model):
    place = (models.CharField(max_length=250, verbose_name="Место выполнения", help_text="Введите Место"),)
    time_to_perform = (models.TimeField(auto_now=True, verbose_name="Время на выполнение", blank=True, null=True),)
    pleasant_habit_flag = (
        models.BooleanField(max_length=250, verbose_name="Признак приятной привычки", help_text="Введите Признак"),
    )

    linked_habit = (
        models.BooleanField(
            max_length=250,
            null=True,
            blank=True,
            verbose_name="Связанная привычка",
        ),
    )
    frequency = models.PositiveIntegerField(default=1, verbose_name="Периодичность")
    reward = models.CharField(
        max_length=250, null=True, blank=True, verbose_name="Вознаграждение ", help_text="Введите Вознаграждение "
    )
    publicity_flag = (models.BooleanField(default=False, verbose_name="Признак публичности"),)
    is_available = (models.BooleanField(default=False, verbose_name="Работает"),)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="habits",
        verbose_name="Создатель привычки",
    )

    def __str__(self):
        return f"{self.pleasant_habit_flag}, {self.linked_habit}"

    def clean(self):
        pass

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        # permissions = [
        #     ("can_unpublish_product", "Can unpublish product"),
        #     ("remove_any_product", "Remove any product"),
        # ]
