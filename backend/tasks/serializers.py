from rest_framework import serializers

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    """Serialize task instances for the API."""

    createdAt = serializers.DateTimeField(
        source="created_at",
        read_only=True,
    )

    class Meta:
        """Configure the fields exposed by the serializer."""

        model = Task
        fields = (
            "id",
            "title",
            "description",
            "priority",
            "status",
            "createdAt",
        )
