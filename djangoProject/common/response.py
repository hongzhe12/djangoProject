import json

from django.http import HttpResponse


def json_response(code: int, message: str, data=None, status: int = 200) -> HttpResponse:
    """统一JSON响应格式"""
    response_data = {"code": code, "message": message}
    if data is not None:
        response_data["data"] = data
    return HttpResponse(json.dumps(response_data, ensure_ascii=False),
                        content_type="application/json", status=status)
