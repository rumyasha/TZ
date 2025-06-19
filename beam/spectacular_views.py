from drf_spectacular.views import SpectacularAPIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse


class SafeSpectacularAPIView(SpectacularAPIView):
    renderer_classes = [JSONRenderer]  # Используем только JSON рендерер

    def get(self, request, *args, **kwargs):
        try:
            response = super().get(request, *args, **kwargs)
            # Принудительно устанавливаем правильный Content-Type
            response['Content-Type'] = 'application/json; charset=utf-8'
            # Убираем заголовок скачивания
            if 'Content-Disposition' in response:
                del response['Content-Disposition']
            return response
        except Exception as e:
            return Response(
                {"error": "Ошибка генерации схемы", "details": str(e)},
                status=500,
                content_type='application/json'
            )