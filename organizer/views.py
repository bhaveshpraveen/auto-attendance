from django.shortcuts import get_object_or_404
from rest_framework import status, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics

from .models import Photo, Course, Teacher, Student
from .serializers import (PhotoSerializer,
                          TeacherSerializer,
                          StudentSerializer,
                          CourseSerializer,
                          CourseListSerializer)
from .utils import generate_random_string, get_current_date, get_unique_identificaton
from . import permissions as custom_permissions


#TODO: Modify Permission Classes
class PhotoUploadViewSet(ModelViewSet):
    # curl --verbose --header "Authorization:
    # jwt eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiMTViY2UwOTA0IiwidXNlcm5hbWUiOiIxNWJjZTA5MDQiLCJleHAiOjE1MjE2NTYzMTEsImVtYWlsIjoiIiwicmVnaXN0cmF0aW9uX251bWJlciI6IjE1YmNlMDkwNCJ9.tVh7p2d-FGlHu-Foh-6ox7BSHo7MNvI15FZbayn7rhE"
    #  --header "Accept: application/json; indent=4" --request POST
    #  --form img=@/Users/bhavesh/Pictures/maxresdefault.jpg http://localhost:8000/api/upload/; echo

    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    parser_classes = (MultiPartParser, FormParser,)
    permission_classes = (permissions.IsAuthenticated, )

    def perform_create(self, serializer):
        print('User is in perform_create=', self.request.user)

        user = self.request.user
        # print('In PhotoUploadViewSet. serializer=', serializer)
        slot = self.request.data.get('slot', None)
        # identification = get_unique_identificaton(serializer)

        if user.is_teacher:
            teacher = user.teacher
            try:
                course = Course.objects.get(teacher=teacher, slot=slot)
            except Course.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer.save(course=course, img=self.request.data.get('img'))
        else:
            print('Student', user.student)

            serializer.save(student=user.student, img=self.request.data.get('img'))


