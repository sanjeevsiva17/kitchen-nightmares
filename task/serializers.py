from rest_framework import serializers
from .models import Task, TaskState
from django.contrib.auth import get_user_model


class TaskSerializer(serializers.ModelSerializer):
    # created_by = serializers.RelatedField(source=get_user_model(), read_only=True)

    class Meta:
        model = Task
        fields = ("id", "title", "priority", "is_active")


class TaskStateSerializer(serializers.ModelSerializer):
    # task = serializers.RelatedField(source="task", read_only=True)
    # accepted_by = serializers.RelatedField(source=get_user_model(), read_only=True)

    class Meta:
        model = TaskState
        fields = ("task", "accepted_by", "state")
