from unittest.mock import patch

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from .models import Task
from .services.ai import AIProviderError


class TaskStatusUpdateAPITest(TestCase):
    """Test the task status update endpoint."""

    def setUp(self) -> None:
        """Create the API client and a test task."""
        self.client = APIClient()
        self.task = Task.objects.create(
            title="Review customer application",
            description="Application is ready for operational review.",
            priority=Task.Priority.MEDIUM,
        )

    def test_valid_status_update(self) -> None:
        """Update a task when a supported status is submitted."""
        response = self.client.patch(
            f"/api/tasks/{self.task.id}/status/",
            {"status": Task.Status.IN_PROGRESS},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.task.refresh_from_db()

        self.assertEqual(
            self.task.status,
            Task.Status.IN_PROGRESS,
        )

    def test_invalid_status_update(self) -> None:
        """Reject a task status that is not supported."""
        response = self.client.patch(
            f"/api/tasks/{self.task.id}/status/",
            {"status": "INVALID"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.task.refresh_from_db()

        self.assertEqual(
            self.task.status,
            Task.Status.NEW,
        )


class TaskAnalysisAPITest(TestCase):
    """Test the task analysis endpoint."""

    def setUp(self) -> None:
        """Create the API client and a test task."""
        self.client = APIClient()
        self.task = Task.objects.create(
            title="Missing customer document",
            description="The latest payslip is missing.",
            priority=Task.Priority.HIGH,
        )

    @patch(
        "tasks.views.MockAIProvider.analyse",
        side_effect=AIProviderError,
    )
    def test_ai_provider_failure(
        self,
        mock_analyse,
    ) -> None:
        """Return a controlled error when the AI provider fails."""
        response = self.client.post(
            f"/api/tasks/{self.task.id}/analyse/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_503_SERVICE_UNAVAILABLE,
        )

        self.assertEqual(
            response.json(),
            {"detail": "AI analysis is currently unavailable."},
        )

        mock_analyse.assert_called_once()
