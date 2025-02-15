# from users import serializers
#
#
# def validate(self, attrs):
#     linked_habit = attrs.get("linked_habit")
#     pleasant_habit_flag = attrs.get("pleasant_habit_flag")
#     time_to_perform = attrs.get("time_to_perform")
#     frequency = attrs.get("frequency")
#     reward = attrs.get("reward")
#
#     def simultaneous_habits(self, attrs):
#         if linked_habit and pleasant_habit_flag:
#             raise serializers.ValidationError("Привычки не могут быть активны одновременно")
#
#     def time_habits(self, attrs):
#         if time_to_perform > 120:
#             raise serializers.ValidationError("Время выполнения не должно быть больше 120 минут.")
#
#     def frequency_habits(self, attrs):
#         if frequency > 7:
#             raise serializers.ValidationError("Периодичность выполнения должна быть от 1 до 7 дней")
#
#     def habit_without_reward(self, attrs):
#         if pleasant_habit_flag and linked_habit:
#             raise serializers.ValidationError(
#                 "У приятной привычки не может быть вознаграждения или связанной привычки"
#             )
#
#     def habit_without_reward1(self, attrs):
#         if pleasant_habit_flag and linked_habit:
#             raise serializers.ValidationError(
#                 "У приятной привычки не может быть вознаграждения или связанной привычки"
#             )
#
#     def associated_habit_without_reward(self, attrs):
#         if linked_habit and reward:
#             raise serializers.ValidationError("У связанной привычки не может быть вознаграждения")
#
#     return attrs
