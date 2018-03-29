from django.shortcuts import get_object_or_404

from rest_framework import (
    status,
    permissions,
    generics
)
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import FormParser, MultiPartParser
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
    course_queryset = Course.objects.all()
    serializer_class = PhotoSerializer
    parser_classes = (MultiPartParser, FormParser,)
    permission_classes = [
        Or(
            And(
                Or(custom_permissions.IsGet, custom_permissions.IsHead, custom_permissions.IsOptions, custom_permissions.IsPost,),
                permissions.IsAuthenticated
            ),
            And(
                Or(custom_permissions.IsDelete, custom_permissions.IsPatch, custom_permissions.IsPut),
                custom_permissions.IsPhotoOwner,
            ),
        )
    ]

    def perform_create(self, serializer):
        print('User is in perform_create=', self.request.user)

        user = self.request.user
        # print('In PhotoUploadViewSet. serializer=', serializer)
        slot = self.request.data.get('slot', None)
        # identification = get_unique_identificaton(serializer)

        if user.is_teacher:
            teacher = user.teacher
            course = get_object_or_404(self.course_queryset, teacher=teacher, slot=slot)
            serializer.save(course=course, img=self.request.data.get('img'))
        else:
            print('Student', user.student)

            serializer.save(student=user.student, img=self.request.data.get('img'))


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


# #TODO: Permissions
# class TeacherDetailView(GetObjectMixin):
#     """Return the courses taken by the teacher"""
#     model = Teacher
#     serializer_class = TeacherSerializer
#     permissions = (permissions.IsAuthenticated, )


# #TODO: Permissions
# class StudentDetailView(GetObjectMixin):
#     """Return the courses taken by student and the link to his pictures"""
#     model = Student
#     serializer_class = StudentSerializer
#     permissions = (permissions.IsAuthenticated,)


# #TODO: Permissions
# class CourseListView(generics.ListAPIView):
#     queryset = Course.objects.all()
#     serializer_class = CourseListSerializer
#     permissions = (permissions.IsAuthenticated,)


#TODO: Permissions
class CourseViewSet(ModelViewSet):
    model = Course
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_object(self):
        user = self.request.user
        obj = self.model.objects.get(user=user)
        self.check_object_permissions(self.request, obj)
        return obj


#TODO: Permissions
class StudentViewSet(ModelViewSet, GetObjectTeacherStudentMixin, PermissionTeacherStudentMixin):
    model = Student
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class TeacherViewSet(ModelViewSet, GetObjectTeacherStudentMixin, PermissionTeacherStudentMixin):
    model = Teacher
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer









