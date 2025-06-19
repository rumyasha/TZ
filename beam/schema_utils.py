# beam/schema_utils.py
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

def handle_schema_error(e):
    error_data = {
        "error": "API Schema Generation Error",
        "details": str(e)
    }
    if settings.DEBUG:
        error_data["traceback"] = str(e.__traceback__)
    return Response(error_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)