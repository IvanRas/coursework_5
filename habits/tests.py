from django.contrib.auth import get_user_model
from django.test import TestCase

from habits.models import Habits

# Create your tests here.

User = get_user_model()


class HabitsModelTest(TestCase):
    def setUp(self):
        self. user = User.objects.create_user(username="test_user", password="12345")

    def test_creating_habit(self):
        habits = Habits.objects.create(
            place="место",
            time="14:00:00",
            action="Действие",
            pleasant_habit_flag=True,
            frequency=2,
            reward="Вознаграждение",
            time_to_perform=100,
            publicity_flag=True,
            owner= self.user,
            related_habit="Связанная привычка"
        )
        self.assertIsInstance(habits, Habits)
        self.assertEqual(habits.action, "Действие")
        self.assertEqual(habits.place, "место")
        self.assertEqual(habits.frequency, 2)

    def test_habit_string_representation(self):
        habits = Habits.objects.create(
            place="место",
            time="14:00:00",
            action="Действие",
            pleasant_habit_flag=True,
            frequency=2,
            reward="Вознаграждение",
            time_to_perform=100,
            publicity_flag=True,
            owner= self.user,
            related_habit="Связанная привычка"
        )
        self.assertEqual(str(habits), habits.action)
