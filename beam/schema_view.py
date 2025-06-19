# beam/schema_view.py
from drf_spectacular.views import SpectacularAPIView
from rest_framework.response import Response
from django.http import HttpResponse


class PlainTextSchemaView(SpectacularAPIView):
    def get(self, request, *args, **kwargs):
        # Получаем стандартный ответ
        response = super().get(request, *args, **kwargs)

        # Создаём новый HttpResponse с тем же содержимым
        content = response.content.decode('utf-8')
        return HttpResponse(
            content,
            content_type='text/plain; charset=utf-8',
            status=response.status_code
        )
