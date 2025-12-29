import os
import platform
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "drf_project.settings")

app = Celery("drf_project")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

if platform.system() == "Windows":
    app.conf.worker_pool = "solo"
