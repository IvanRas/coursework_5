from django.shortcuts import render
from rest_framework import viewsets

from atomic_habits import permissions
from atomic_habits.models import Habits
from atomic_habits.permissions import IsModerator


# Create your views here.


class CourseViewSet(viewsets.ModelViewSet):
    """
    управление курсом и проверка разрешений
    """

    queryset = Habits.objects.all()
    # serializer_class =

    def get_permissions(self):
        if self.action in ["create", "destroy"]:
            return [permissions.IsAdminUser()]
        elif self.action in ["list", "retrieve", "update"]:
            return [IsModerator() or permissions.IsAuthenticated()]
        return super().get_permissions()

    # def get_queryset(self):