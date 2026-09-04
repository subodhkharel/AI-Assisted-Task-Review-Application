from django.urls import path

from .views import TaskAnalysisView, TaskListView, TaskStatusUpdateView

urlpatterns = [
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path(
        "tasks/<int:pk>/status/",
        TaskStatusUpdateView.as_view(),
        name="task-status-update",
    ),
    path(
        "tasks/<int:pk>/analyse/",
        TaskAnalysisView.as_view(),
        name="task-analyse",
    ),
]
