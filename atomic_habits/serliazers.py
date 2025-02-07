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