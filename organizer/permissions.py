from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsTeacher(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_teacher


class IsStudent(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return not request.user.is_teacher


class IsTeachersCourse(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.teacher == request.user
    

