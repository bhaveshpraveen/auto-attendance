from rest_framework import serializers
from .models import Photo, Course


class PhotoSerializer(serializers.HyperlinkedModelSerializer):
    student = serializers.SlugRelatedField(read_only=True, slug_field='id')
    course = serializers.SlugRelatedField(read_only=True, slug_field='id')

    class Meta:
        model = Photo
        fields = '__all__'
        read_only_fields = ('course', 'student', 'created', 'identification', 'img')


class CourseSerializer(serializers.ModelSerializer):
    # If you're using the standard router classes this will be a string with the format <modelname>-detail. required.
    photos = serializers.HyperlinkedRelatedField(many=True, view_name='photo-detail', read_only=True)

    class Meta:
        model = Course
        fields = ('course_code', 'course_name', 'slot', 'room', 'teacher', 'photos')


