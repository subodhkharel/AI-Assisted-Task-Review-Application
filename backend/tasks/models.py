from django.db import models


class Task(models.Model):
    """Represent an incoming operational task."""

    class Status(models.TextChoices):
        """Define the supported task statuses."""

        NEW = "NEW", "New"
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        COMPLETED = "COMPLETED", "Completed"

    class Priority(models.TextChoices):
        """Define the supported task priorities."""

        LOW = "LOW", "Low"
        MEDIUM = "MEDIUM", "Medium"
        HIGH = "HIGH", "High"

    title = models.CharField(max_length=255)
    description = models.TextField()
    priority = models.CharField(
        max_length=10,
        choices=Priority.choices,
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """Return a readable representation of the task."""
        return self.title
