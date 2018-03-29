from django.contrib.auth import get_user_model

from rest_framework import serializers
from djoser import serializers as djoser_serializers

User = get_user_model()


class UserSerializer(djoser_serializers.UserSerializer):
    """Changing the Meta class to include the needed fields and inheriting all the functionality of djoser Serializers
    Use these for reference:
    https://github.com/sunscrapers/djoser/blob/master/djoser/conf.py
    https://github.com/sunscrapers/djoser/blob/master/djoser/serializers.py
    Using the above two files as reference, made changes to the `conf.py` file by overiding some
    settings in `settings.py` file.
    """
    class Meta:
        model = User
        fields = ('registration_number', 'is_teacher', 'email', 'first_name', 'last_name')


class UserCreateSerializer(djoser_serializers.UserCreateSerializer):
    """Changing the Meta class to include all fields while inheriting from """
    class Meta:
        model = User
        fields = ('registration_number', 'is_teacher', 'email', 'first_name', 'last_name', 'password')


class UserRegNoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'registration_number', 'first_name', 'last_name')

