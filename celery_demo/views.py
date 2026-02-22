from celery.result import AsyncResult
from djangoProject.celery import app as celery_app
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .tasks import add_numbers, slow_echo


def _parse_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


class EnqueueAddView(APIView):
    def post(self, request):
        a = _parse_int(request.data.get("a"))
        b = _parse_int(request.data.get("b"))
        if a is None or b is None:
            return Response({"detail": "a and b must be integers"}, status=status.HTTP_400_BAD_REQUEST)

        task = add_numbers.delay(a, b)
        return Response({"task_id": task.id, "state": task.state})


class EnqueueEchoView(APIView):
    def post(self, request):
        message = request.data.get("message")
        delay = _parse_int(request.data.get("delay")) or 3
        if not isinstance(message, str) or not message.strip():
            return Response({"detail": "message is required"}, status=status.HTTP_400_BAD_REQUEST)

        task = slow_echo.delay(message.strip(), delay)
        return Response({"task_id": task.id, "state": task.state})


class TaskStatusView(APIView):
    def get(self, request, task_id):
        result = AsyncResult(task_id, app=celery_app)
        payload = {
            "task_id": task_id,
            "state": result.state,
            "ready": result.ready(),
        }

        if result.successful():
            payload["result"] = result.result
        elif result.failed():
            payload["error"] = str(result.result)
        else:
            payload["info"] = str(result.info) if result.info else None

        return Response(payload)
