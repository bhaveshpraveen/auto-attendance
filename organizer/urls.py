from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'upload', views.PhotoUploadViewSet)

urlpatterns = [
    re_path('^', include(router.urls))
]

