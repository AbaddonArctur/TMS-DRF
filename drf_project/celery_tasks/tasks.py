import logging
from celery import shared_task
from django.utils import timezone
from django.db import transaction

from .models import TaskRunCounter

logger = logging.getLogger(__name__)

@shared_task
def example_task():
    with transaction.atomic():
        counter, _ = TaskRunCounter.objects.select_for_update().get_or_create(task_name="example_task")
        counter.runs += 1
        counter.save()

        logger.info("Executed for the %s time at %s",counter.runs, timezone.localtime(timezone.now()),)