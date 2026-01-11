from django.urls import path

from .views import RunExampleTaskView

urlpatterns = [
    path("run-example-task/", RunExampleTaskView.as_view()),
]
