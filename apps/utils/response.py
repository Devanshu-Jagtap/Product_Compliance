# utils/response.py

from rest_framework.response import Response
from rest_framework import status

def api_response(
    message="",
    data=None,
    success=True,
    code=status.HTTP_200_OK,
    errors=None,
    extra=None
):

    res = {
        "status": "success" if success else "failed",
        "message": message,
        "code": code,
        "data": data if success else None,
        "errors": errors if not success else None
    }

    if extra:
        res.update(extra)

    return Response(res, status=code)
