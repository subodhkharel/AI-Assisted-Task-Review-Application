from rest_framework import generics
from rest_framework.exceptions import ValidationError

from .models import Task
from .serializers import TaskSerializer


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
