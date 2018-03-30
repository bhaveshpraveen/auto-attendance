from rest_framework import serializers

from core.serializers import UserRegNoSerializer
from .models import Photo, Course, Teacher, Student


class PhotoSerializer(serializers.HyperlinkedModelSerializer):
    student = serializers.SlugRelatedField(read_only=True, slug_field='id')
    course = serializers.SlugRelatedField(read_only=True, slug_field='id')

    class Meta:
        model = Photo
        fields = ('id', 'course', 'student', 'identification', 'img')
        read_only_fields = ('id', 'img', 'identification', 'course', 'student', 'timestamp', )


class CourseSerializer(serializers.ModelSerializer):
    teacher = serializers.StringRelatedField()
    # If you're using the standard router classes this will be a string with the format <modelname>-detail.
    photos = serializers.HyperlinkedRelatedField(many=True, view_name='photo-detail', read_only=True)
    # students = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ('id', 'course_code', 'course_name', 'slot', 'room', 'venue', 'photos', 'teacher')


class TeacherSerializer(serializers.ModelSerializer):
    courses = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # students = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Teacher
        fields = ('user', 'courses')


class StudentSerializer(serializers.ModelSerializer):
    # Here, changing the user serializer from the default one because when rendering the students list,
    # is rather tedious if you were send a request for every user
    user = UserRegNoSerializer()
    courses = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    photos = serializers.HyperlinkedRelatedField(many=True, view_name='photo-detail', read_only=True)

    class Meta:
        model = Student
        fields = ('user', 'courses', 'photos')


class StudentListSerializer(serializers.ModelSerializer):
    user = UserRegNoSerializer()

    class Meta:
        model = Student
        fields = ('user', )

