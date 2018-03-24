from rest_framework import serializers
from .models import Photo, Course, Teacher, Student


class PhotoSerializer(serializers.HyperlinkedModelSerializer):
    student = serializers.SlugRelatedField(read_only=True, slug_field='id')
    course = serializers.SlugRelatedField(read_only=True, slug_field='id')

    class Meta:
        model = Photo
        fields = '__all__'
        read_only_fields = ('course', 'student', 'created', 'identification', 'img')


class CourseSerializer(serializers.ModelSerializer):
    # If you're using the standard router classes this will be a string with the format <modelname>-detail.
    photos = serializers.HyperlinkedRelatedField(many=True, view_name='photo-detail', read_only=True)

    class Meta:
        model = Course
        fields = ('course_code', 'course_name', 'slot', 'room', 'teacher', 'photos')


class TeacherSerializer(serializers.ModelSerializer):
    courses = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    students = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Teacher
        fields = ('user', 'courses')


class StudentSerializer(serializers.ModelSerializer):
    courses = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    photos = serializers.HyperlinkedRelatedField(many=True, view_name='photo-detail', read_only=True)

    class Meta:
        model = Student
        fields = ('user', 'courses', 'photos')
