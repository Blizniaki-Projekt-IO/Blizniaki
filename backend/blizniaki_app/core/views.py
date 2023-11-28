import os
from wsgiref.util import FileWrapper

from django.http import HttpResponse, JsonResponse, FileResponse
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from blizniaki_app import settings
from core.models import Face
from core.neurons.predictor import predict
from core.serializer import FaceSerializer
from core.utils.report import create_report


class FaceUploadView(CreateAPIView):
    queryset = Face.objects.all()
    serializer_class = FaceSerializer

    def post(self, request, *args, **kwargs):
        image = request.data["image"]
        face = Face.objects.create(image=image)
        request.session["face_id"] = face.pk
        return HttpResponse({"message": "Twarz utworzona poprawnie!"}, status=200)


class QuizUploadView(APIView):
    def post(self, request):
        face = Face.objects.get(pk=request.session.get("face_id"))
        del request.session["face_id"]
        answers = request.data.get("character")
        result = predict(face.image.name, answers)
        raport = create_report(result)
        face.raport_url = raport
        face.save()
        return JsonResponse({
            "result": result,
            "raport": raport,
        })


class DownloadReportView(APIView):
    def post(self, request):
        report_url = request.data["report_url"]
        report = open(os.path.join(settings.MEDIA_ROOT, report_url), 'rb')
        response = HttpResponse(FileWrapper(report), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename={report_url.replace("reports/", "")}'
        return response
