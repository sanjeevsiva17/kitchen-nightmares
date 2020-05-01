from django.shortcuts import render
from rest_framework import viewsets
from .serializers import TaskSerializer, TaskStateSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import Task, TaskState


# Create your views here.

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        """Creating a post"""
        serializer.save(created_by=self.request.user)


class TaskStateViewSet(viewsets.ModelViewSet):
    serializer_class = TaskStateSerializer
    queryset = TaskState.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(accepted_by=self.request.user)
