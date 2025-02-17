from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status

from habits.models import Habits
from rest_framework.test import APIClient

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
            owner=self.user,
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
            owner=self.user,
            related_habit="Связанная привычка"
        )
        self.assertEqual(str(habits), habits.action)


class HabitAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="test_user", password="12345")
        self.client.force_authenticate(user=self.user)

        self.habits = Habits.objects.create(
            place="место",
            time="14:00:00",
            action="Действие",
            pleasant_habit_flag=True,
            frequency=2,
            reward="Вознаграждение",
            time_to_perform=100,
            owner=self.user,
            related_habit="Связанная привычка"
        )

    def test_create_habit(self):
        response = self.client.post(
            "/habits/create/",
            {
                "place": "место",
                "time": "14:00:00",
                "action": "Действие",
                "pleasant_habit_flag": True,
                "frequency": 2,
                "reward": "Вознаграждение",
                "time_to_perform": 100,
                "owner": 100,
                "related_habit": "Связанная привычка",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["action"], "Чтение")

    def test_update_habit(self):
        response = self.client.patch(
            f"/habits/edit/{self.habits.id}/",
            {"action": "Другое действие", "frequency": 5},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.habit.refresh_from_db()
        self.assertEqual(self.habits.action, "Другое действие")
        self.assertEqual(self.habits.frequency, 5)

    def test_delete_habit(self):
        response = self.client.delete(f"/habits/delete/{self.habit.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Habits.objects.filter(id=self.habit.id).exists())

    def test_list_user_habits(self):
        response = self.client.get("/habits/list/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_public_habits(self):
        public_habit = Habits.objects.create(
            owner=self.user,
            place="дом",
            time="07:00:00",
            action="зарядка",
            is_pleasant=True,
            frequency=1,
            reward=None,
            time_to_complete=120,
            is_public=True,
        )
        response = self.client.get("/habits/list/public/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(public_habit.action, [habits["action"] for habits in response.data])
