import base64
import json
import os
from wsgiref.util import FileWrapper

from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
from rest_framework.response import Response

from blizniaki_app import settings
from core.models import Face
from core.neurons.predictor import predict
from core.serializer import FaceSerializer
from core.utils.report import create_report


class FaceUploadView(CreateAPIView):
    queryset = Face.objects.all()
    serializer_class = FaceSerializer
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        image = request.data["image"]
        face = Face.objects.create(image=image)
        return JsonResponse({"face_id": face.pk}, status=200)


class QuizUploadView(APIView):
    def post(self, request):
        try:
            face = Face.objects.get(pk=request.data.get("face_id"))
            answers = request.data.get("character")
            result = predict(face.image.name, answers)
            raport = create_report(result)
            face.raport_url = raport.get("raport_pdf")
            face.save()
            return JsonResponse({
                "result": result,
                "raport": raport,
            })
        except Face.DoesNotExist:
            return JsonResponse({
                "error": "Face id nie pasuje",
            }, status=401)


class DownloadReportPDFView(APIView):
    def get(self, request):
        report_url = request.GET.get("report_url")
        report = open(os.path.join(settings.MEDIA_ROOT, report_url), 'rb')
        response = HttpResponse(FileWrapper(report), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename={report_url.replace("reports/", "")}'
        return response


class DownloadReportHTMLView(APIView):
    def get(self, request):
        report_url = request.GET.get("report_url")
        report = open(os.path.join(settings.MEDIA_ROOT, report_url), 'rb')
        response = HttpResponse(FileWrapper(report), content_type='html')
        response['Content-Disposition'] = f'attachment; filename={report_url.replace("reports/", "")}'
        return response
