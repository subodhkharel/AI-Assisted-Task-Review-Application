from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework import generics
from .models import Task
from .serializers import TaskSerializer
from .serializers import TaskSerializer, TaskStatusUpdateSerializer

class TaskListView(generics.ListAPIView):
    """Return tasks with optional status filtering."""

    serializer_class = TaskSerializer

    def get_queryset(self):
        """Return tasks filtered by the requested status."""
        queryset = Task.objects.all().order_by("-created_at")

        status = self.request.query_params.get("status")

        if status is None:
            return queryset

        valid_statuses = {
            choice.value for choice in Task.Status
        }

        if status not in valid_statuses:
            raise ValidationError(
                {
                    "status": (
                        "Invalid status. "
                        f"Expected one of: {', '.join(sorted(valid_statuses))}."
                    )
                }
            )

        return queryset.filter(status=status)


class TaskStatusUpdateView(generics.UpdateAPIView):
    """Update the status of an existing task."""

    queryset = Task.objects.all()
    serializer_class = TaskStatusUpdateSerializer
    http_method_names = ["patch"]
