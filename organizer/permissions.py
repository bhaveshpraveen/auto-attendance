from rest_framework import permissions


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsTeacher(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user.is_teacher
