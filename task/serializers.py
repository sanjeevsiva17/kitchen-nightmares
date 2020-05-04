from rest_framework import serializers
from .models import Task, TaskState
# from django.contrib.auth import get_user_model
from users.serializers import UserSerializer, UserSerializer2


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ("id", "title", "priority", "is_active")


class TaskSerializer2(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField()

    class Meta:
        model = Task
        fields = ("id", "title", "priority", "is_active", "created_by")


class TaskStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskState
        fields = ("task", "accepted_by", "state")


class TaskStateSerializerStoreManager(serializers.ModelSerializer):
    task = TaskSerializer2()
    accepted_by = UserSerializer2()

    class Meta:
        model = TaskState
        fields = ("task", "accepted_by", "state", )


class TaskStateSerializerDeliveryGuy(serializers.ModelSerializer):
    task = TaskSerializer2()
    accepted_by = UserSerializer()

    class Meta:
        model = TaskState
        fields = ("task", "accepted_by", "state", )
