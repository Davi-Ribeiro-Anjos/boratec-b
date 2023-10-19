import os

from django.http import FileResponse
from django.conf import settings

from rest_framework.views import APIView, Response, Request


def get_media(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)

    if os.path.exists(file_path):
        extension = file_path.split("/")[-1].split(".")[1]

        if extension == "pdf":
            content_type = "application/pdf"
        elif extension == "png":
            content_type = "application/png"
        else:
            content_type = "application/octet-stream"

        return FileResponse(open(file_path, "rb"), content_type=content_type)
    else:
        from django.http import HttpResponseNotFound

        return HttpResponseNotFound()


class GetMediaView(APIView):
    def post(self, request: Request, path: str) -> Response:
        return get_media(request, path)
