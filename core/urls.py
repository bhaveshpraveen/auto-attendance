from django.urls import path, include
from djoser import views as djoser_views
from rest_framework_jwt import views as jwt_views

from . import views

urlpatterns = [
    path('user/view/', djoser_views.UserView.as_view(), name='user-view'),
    path('user/delete/', djoser_views.UserDeleteView.as_view(), name='user-delete'),
    path('user/create/', djoser_views.UserCreateView.as_view(), name='user-create'),
    # Views are defined in Rest Framework JWT, but we're assigning custom paths.
    path('user/login/', jwt_views.ObtainJSONWebToken.as_view(), name='user-login'),
    path('user/login/refresh/', jwt_views.RefreshJSONWebToken.as_view(), name='user-login-refresh'),
    path('user/logout/all/', views.UserLogoutAllView.as_view(), name='user-logout-all'),
]