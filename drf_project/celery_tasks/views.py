from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .tasks import example_task


class RunExampleTaskView(APIView):
    def post(self, request):
        task = example_task.delay()

        return Response(
            {
                "task_id": task.id,
                "status": "task sent to celery",
            },
            status=status.HTTP_202_ACCEPTED,
        )
