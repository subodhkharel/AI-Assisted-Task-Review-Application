from tasks.models import Task

from .ai import AIProvider, TaskAnalysis


class TaskAnalysisService:
    """Coordinate task analysis through an AI provider."""

    def __init__(self, provider: AIProvider) -> None:
        """Initialize the service with an AI provider."""
        self.provider = provider

    def analyse(self, task: Task) -> TaskAnalysis:
        """Analyse the provided task using the configured AI provider."""
        return self.provider.analyse(task)
