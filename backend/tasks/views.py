from rest_framework.exceptions import ValidationError
from .models import Task
from .serializers import (
    TaskSerializer,
    TaskStatusUpdateSerializer,
    TaskAnalysisSerializer,
)
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .services.ai import AIProviderError, MockAIProvider
from .services.analysis import TaskAnalysisService


class TaskListView(generics.ListAPIView):
    """Return tasks with optional status filtering."""

    serializer_class = TaskSerializer

    def get_queryset(self):
        """Return tasks filtered by the requested status."""
        queryset = Task.objects.all().order_by("-created_at")

        status = self.request.query_params.get("status")

        if status is None:
            return queryset

        valid_statuses = {choice.value for choice in Task.Status}

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


class TaskAnalysisView(APIView):
    """Analyse an existing task using the configured AI provider."""

    def post(self, request, pk: int):
        """Analyse the requested task and return structured AI output."""
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response(
                {"detail": "Task not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        service = TaskAnalysisService(
            provider=MockAIProvider(),
        )

        try:
            analysis = service.analyse(task)
        except AIProviderError:
            return Response(
                {"detail": "AI analysis is currently unavailable."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        serializer = TaskAnalysisSerializer(
            data={
                "category": analysis.category,
                "priority": analysis.priority,
                "summary": analysis.summary,
                "recommendedAction": analysis.recommended_action,
            },
        )

        if not serializer.is_valid():
            return Response(
                {"detail": "AI returned an invalid analysis."},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        return Response(
            serializer.validated_data,
            status=status.HTTP_200_OK,
        )
