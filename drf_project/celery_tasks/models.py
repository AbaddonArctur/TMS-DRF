from django.db import models

class TaskRunCounter(models.Model):
    task_name = models.CharField(max_length=255, unique=True)
    runs = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.task_name}: {self.runs}"