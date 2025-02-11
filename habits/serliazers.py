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

    def validate_choice(self, linked_habit, pleasant_habit_flag, time_to_perform, frequency, reward):
        """
        соблюдение условий привыячек
        """
        if linked_habit and pleasant_habit_flag:
            raise serializers.ValidationError("Привычки не могут быть активны одновременно")
        if time_to_perform > 120:
            raise serializers.ValidationError("Время выполнения не должно быть больше 120 минут.")
        if frequency < 1 or frequency > 7:
            raise serializers.ValidationError("Периодичность выполнения должна быть от 1 до 7 дней")
        if pleasant_habit_flag == 1 and linked_habit == 1 or reward == 1:
            raise serializers.ValidationError(
                "У приятной привычки не может быть вознаграждения или связанной привычки"
            )
        if linked_habit == reward:
            raise serializers.ValidationError("У связанной привычки не может быть вознаграждения")
