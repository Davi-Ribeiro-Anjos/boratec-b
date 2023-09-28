from django.http import FileResponse
from django.conf import settings
import os


def get_media(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    print("aqui")
    if os.path.exists(file_path):
        return FileResponse(
            open(file_path, "rb"), content_type="application/octet-stream"
        )
    else:
        from django.http import HttpResponseNotFound

        return HttpResponseNotFound()
