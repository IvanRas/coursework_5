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
        fields = "linked_habit, pleasant_habit_flag, time_to_perform, frequency, reward"
        read_only_fields = ["owner"]

    def choice(self, linked_habit, pleasant_habit_flag, time_to_perform, frequency, reward):
        """
        соблюдение условий привыячек
        """
        if linked_habit == 1 and pleasant_habit_flag == 1:
            raise serializers.ValidationError("Привычки не могут быть активны одновременно")
        if time_to_perform > 120:
            raise serializers.ValidationError("Время выполнения не должно быть больше 120 минут.")
        if frequency < 1 or frequency > 7:
            raise serializers.ValidationError("Периодичность выполнения должна быть от 1 до 7 дней")
        if pleasant_habit_flag == 1 and linked_habit == 1 or reward == 1:
            raise serializers.ValidationError("У приятной привычки не может быть вознаграждения или связанной привычки")
