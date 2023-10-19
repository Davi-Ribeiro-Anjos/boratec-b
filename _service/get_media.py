import os

from django.http import FileResponse
from django.conf import settings

from rest_framework.views import APIView, Response, Request, status


def get_media(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)

    if os.path.exists(file_path):
        return FileResponse(
            open(file_path, "rb"), content_type="application/octet-stream"
        )
    else:
        from django.http import HttpResponseNotFound

        return HttpResponseNotFound()


class GetMediaView(APIView):
    def get(self, request: Request, path: str) -> Response:
        return get_media(request, path)
