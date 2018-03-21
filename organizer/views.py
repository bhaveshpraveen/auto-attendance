from rest_framework import status, permissions
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Photo, Course
from .serializers import PhotoSerializer
from .utils import generate_random_string, get_current_date, get_unique_identificaton


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
        print('User=', self.request.user)

        # print('In PhotoUploadViewSet. serializer=', serializer)
        course_code = self.request.data.get('course_code', None)
        slot = self.request.data.get('slot', None)
        # identification = get_unique_identificaton(serializer)

        if self.request.user.is_teacher:
            teacher = self.request.user.teacher
            try:
                course = Course.objects.get(course_code=course_code, slot=slot, teacher=teacher)
            except Course.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

            serializer.save(course=course, teacher=teacher)
            # serializer.save(course= )
        else:
            print('Student', self.request.user.student)

            serializer.save(student=self.request.user.student, img=self.request.data.get('img'))
