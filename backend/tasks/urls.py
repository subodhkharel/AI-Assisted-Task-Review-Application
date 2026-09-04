from django.urls import path

from .views import TaskListView, TaskStatusUpdateView

urlpatterns = [
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path(
        "tasks/<int:pk>/status/",
        TaskStatusUpdateView.as_view(),
        name="task-status-update",
    ),
]
