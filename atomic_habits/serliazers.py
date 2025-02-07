from rest_framework import serializers
from .models import Habits


class HabitsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Habits
        fields = "__all__"
        read_only_fields = ["owner"]

    def create(self, validated_data):
        # Устанавливаем текущего пользователя как владельца привычки
        validated_data["owner"] = self.context["request"].user
        # Применяем валидацию при создании
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Применяем валидацию при обновлении
        return super().update(instance, validated_data)


class Habits_Is_Available(serializers.ModelSerializer):
    class Meta:
        model = Habits
        fields = "pleasant_habit_flag, linked_habit"
        read_only_fields = ["owner"]

    def choice(self, linked_habit, pleasant_habit_flag):
        """
        если одна из привычек активна вторая неактивна
        """
        if linked_habit == 1 and pleasant_habit_flag == 1:
            raise serializers.ValidationError("Привычки не могут быть активны одновременно")
