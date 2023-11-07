import json

from django.http import HttpResponse
from rest_framework.generics import CreateAPIView

from blizniaki_app import settings
from core.models import Face
from core.serializer import FaceSerializer


class FaceUploadView(CreateAPIView):
    queryset = Face.objects.all()
    serializer_class = FaceSerializer

    def post(self, request, *args, **kwargs):
        image = request.data["image"]
        path = str(f"{settings.MEDIA_ROOT}/{image.name}")
        # dalsza ścieżka - przekazanie zdjęcia do funkcji czytającej wytrenowany model
        # zwrot: json z gotowym predictem
        return HttpResponse(json.dumps({"message": "zdjęcie wrzucone poprawnie"}), status=200)
