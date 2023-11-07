from rest_framework import serializers

from core.models import Face


class FaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Face
        fields = ('image',)