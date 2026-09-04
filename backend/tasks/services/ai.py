from dataclasses import dataclass
from typing import Protocol

from tasks.models import Task


@dataclass(frozen=True)
class TaskAnalysis:
    """Represent the structured result returned by an AI analysis."""

    category: str
    priority: str
    summary: str
    recommended_action: str


class AIProvider(Protocol):
    """Define the interface required by an AI provider."""

    def analyse(self, task: Task) -> TaskAnalysis:
        """Analyse a task and return structured analysis."""
        ...


class MockAIProvider:
    """Provide deterministic AI-like analysis for local development."""

    def analyse(self, task: Task) -> TaskAnalysis:
        """Analyse a task using simple mock rules."""
        description = task.description.lower()
        title = task.title.lower()

        if "payslip" in description or "document" in title:
            return TaskAnalysis(
                category="DOCUMENT_REQUEST",
                priority="HIGH",
                summary=(
                    "Customer needs to provide the missing document "
                    "required for their application."
                ),
                recommended_action="Request the missing document from the customer.",
            )

        if "contact" in title or "phone number" in description:
            return TaskAnalysis(
                category="CUSTOMER_CONTACT",
                priority=task.priority,
                summary="Customer contact information needs to be updated.",
                recommended_action="Review and update the customer's contact information.",
            )

        return TaskAnalysis(
            category="GENERAL",
            priority=task.priority,
            summary="The task requires operational review.",
            recommended_action="Review the task details and determine the appropriate action.",
        )
