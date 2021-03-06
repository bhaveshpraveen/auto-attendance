from bson.json_util import dumps
from pymongo import MongoClient

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.conf import settings

from rest_framework import (
    status,
    permissions,
    generics
)
from rest_framework.decorators import list_route, detail_route
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from rest_condition import And, Or, Not

from .models import (
    Photo,
    Course, Teacher,
    Student
)
from .serializers import (PhotoSerializer,
                          TeacherSerializer,
                          StudentSerializer,
                          StudentListSerializer,
                          CourseSerializer,)

from . import permissions as custom_permissions
from face_detect.tasks import process_photo


class PhotoUploadViewSet(ModelViewSet):
    # curl --verbose --header "Authorization:
    # jwt eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiMTViY2UwOTA0IiwidXNlcm5hbWUiOiIxNWJjZTA5MDQiLCJleHAiOjE1MjE2NTYzMTEsImVtYWlsIjoiIiwicmVnaXN0cmF0aW9uX251bWJlciI6IjE1YmNlMDkwNCJ9.tVh7p2d-FGlHu-Foh-6ox7BSHo7MNvI15FZbayn7rhE"
    #  --header "Accept: application/json; indent=4" --request POST
    #  --form img=@/Users/bhavesh/Pictures/maxresdefault.jpg http://localhost:8000/api/upload/; echo

    queryset = Photo.objects.all()
    course_queryset = Course.objects.all()
    serializer_class = PhotoSerializer
    parser_classes = (MultiPartParser, FormParser,)
    permission_classes = [
        Or(
            And(
                Or(custom_permissions.IsGet,
                   custom_permissions.IsHead,
                   custom_permissions.IsOptions,
                   custom_permissions.IsPost),
                permissions.IsAuthenticated
            ),
            And(
                Or(custom_permissions.IsDelete,
                   custom_permissions.IsPatch,
                   custom_permissions.IsPut),
                custom_permissions.IsPhotoOwner,
            ),
        )
    ]

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if user.is_teacher:
            return qs.filter(course__teacher=user.teacher)
        return qs.filter(student=user.student)

    def perform_create(self, serializer):
        print('User is in perform_create=', self.request.user)

        user = self.request.user
        # print('In PhotoUploadViewSet. serializer=', serializer)
        _id = self.request.data.get('id')
        # identification = get_unique_identificaton(serializer)

        if user.is_teacher:
            teacher = user.teacher
            course = get_object_or_404(self.course_queryset, teacher=teacher, id=_id)
            obj = serializer.save(course=course, img=self.request.data.get('img'))
        else:
            print('Student', user.student)

            obj = serializer.save(student=user.student, img=self.request.data.get('img'))

        process_photo.delay(obj.id)
        # process_photo(obj.id)


class GetObjectTeacherStudentMixin:
    def get_object(self):
        obj = self.model.objects.get(user=self.request.user)
        self.check_object_permissions(self.request, obj)
        return obj


class PermissionTeacherStudentMixin:
    permissions_classes = [
        Or(
            And(
                Or(custom_permissions.IsGet, custom_permissions.IsHead, custom_permissions.IsOptions),
                permissions.IsAuthenticated
            ),
            And(
                # If the method is post, permission will always be denied. Since Teacher Model extends from User model
                custom_permissions.IsPost,
                custom_permissions.NoPermission
            ),
            And(
                Or(custom_permissions.IsPatch, custom_permissions.IsPut, custom_permissions.IsDelete),
                custom_permissions.IsOwner
            )
        )
    ]


class CourseViewSet(ModelViewSet):
    model = Course
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    student_serializer = StudentListSerializer
    permission_classes = [
        Or(
            And(
                Or(custom_permissions.IsGet, custom_permissions.IsHead, custom_permissions.IsOptions),
                permissions.IsAuthenticated
            ),
            # Student should not be able to modify any other field
            And(custom_permissions.IsPatch, custom_permissions.IsStudent, custom_permissions.IsFields()),
            And(custom_permissions.IsPost, custom_permissions.IsTeacher),
            # teacher can modify his course
            And(custom_permissions.IsTeacher, custom_permissions, custom_permissions.IsPut, custom_permissions.IsPatch, custom_permissions.IsCourseTeacher),
        )
    ]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(teacher=user.teacher)

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if (not user.is_teacher) and self.request.method == "PATCH":
            # If method is PATCH, return the queryset as is, in order to enroll
            return qs
        if user.is_teacher:
            # if user is requesting, then send only the objects he can modify
            return user.teacher.courses.all()
        # Send only the courses student has enrolled
        return user.student.courses.all()

    @list_route(methods=['get'], url_path='all')
    def all_courses(self, request):
        queryset = self.queryset
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @detail_route(methods=['get'], url_path='attendance')
    def fetch_attendance(self, request, pk=None):
        obj = self.get_object()
        course_code = obj.course_code
        slot = obj.slot
        teacher = obj.teacher.user.registration_number

        client = MongoClient(settings.URI)
        db = client['attendance']
        collection = db['attendance']
        data = dumps(collection.find({
            'teacher': teacher,
            'slot': slot,
            'course_code': course_code
        }))

        return HttpResponse(data)

    def perform_update(self, serializer):
        user = self.request.user
        course = serializer.save()
        if not user.is_teacher:
            # Enrolling the student to the course
            course.students.add(user.student)

    @detail_route(methods=['get'], url_path='students')
    def enrolled_students(self, request, pk=None):
        """Returns a list of students enrolled in a course"""
        obj = self.get_object()
        students = obj.students.all()
        serializer = self.student_serializer(students, many=True)
        return Response(serializer.data)


class StudentViewSet(ModelViewSet, GetObjectTeacherStudentMixin, PermissionTeacherStudentMixin):
    model = Student
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class TeacherViewSet(ModelViewSet, GetObjectTeacherStudentMixin, PermissionTeacherStudentMixin):
    model = Teacher
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer



# to find the location of the file
# https://stackoverflow.com/questions/48146443/resize-crop-an-image-using-celery-in-django-in-django-admin-and-outside





