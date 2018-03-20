from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.viewsets import ModelViewSet
from .models import Photo, Course, Student
from .serializers import PhotoSerializer


class FileUploadViewSet(ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = Photo
    parser_classes = (MultiPartParser, FormParser,)

    # def perform_create(self, serializer):
    #     if self.request.user.is_teacher:
    #          course = Course.objects.get(pk=self.serializer)
    #         serializer.save(course=course)
    #     else:
    #         self.request.
    #     serializer.save(owner=self.request.user,
    #                     img=self.request.data.get('img'))