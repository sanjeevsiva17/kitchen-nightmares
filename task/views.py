from django.shortcuts import render
from rest_framework import viewsets
from .serializers import TaskSerializer, TaskStateSerializer, TaskStateSerializerStoreManager, \
    TaskStateSerializerDeliveryGuy
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import Task, TaskState
from rest_framework.response import Response
from rest_framework import generics
from django.db import transaction


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
        with transaction.atomic():
            task = serializer.save(created_by=self.request.user)
            TaskState.objects.create(task=task)


class TaskStateViewSet(viewsets.ModelViewSet):
    serializer_class = TaskStateSerializer
    queryset = TaskState.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    # def get_queryset(self):
    #     return self.queryset.filter(accepted_by=self.request.user)

    def perform_update(self, serializer):
        if serializer.validated_data['state'] == 'ACC':
            serializer.instance.accepted()
        elif serializer.validated_data['state'] == 'COM':
            serializer.instance.completed()
        elif serializer.validated_data['state'] == 'DEC':
            serializer.instance.declined()
        elif serializer.validated_data['state'] == 'CAN':
            serializer.instance.canceled()

        serializer.instance.accepted_by = self.request.user
        serializer.instance.save()
        print("update")


class TaskwithState(generics.ListAPIView):
    # serializer_class = TaskStateSerializer2
    queryset = TaskState.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.request.user.role == 'R':
            self.serializer_class = TaskStateSerializerStoreManager
            return self.queryset.filter(task__created_by=self.request.user)
        else:
            self.serializer_class = TaskStateSerializerDeliveryGuy
            return self.queryset.filter(accepted_by=self.request.user)
