from rest_framework import serializers
from .models import Photo


class PhotoSerializer(serializers.HyperlinkedModelSerializer):
    course = serializers.PrimaryKeyRelatedField()
    student = serializers.PrimaryKeyRelatedField()

    class Meta:
        model = Photo
        read_only_fields = ('course', 'student', 'created', 'identification', 'img')
