from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

router = DefaultRouter()
router.register(r'photo', views.PhotoUploadViewSet)
router.register(r'course', views.CourseViewSet)
router.register(r'student', views.StudentViewSet)
router.register(r'teacher', views.TeacherViewSet)


# non_router_urls = [
#     path('teacher/', views.TeacherDetailView.as_view()),
#     path('student/', views.StudentDetailView.as_view()),
#     path('course/list/', views.CourseListView.as_view()),
# ]

# non_router_urls = format_suffix_patterns(non_router_urls)

urlpatterns = [
    # re_path('^', include(non_router_urls)),
    re_path('^', include(router.urls)),
]

