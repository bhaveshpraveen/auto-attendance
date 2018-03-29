from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_teacher


class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_teacher


class IsTeachersCourse(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.teacher == request.user


class NoPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return False


class IsAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated()


class IsPost(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method == 'POST'


class IsGet(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method == 'GET'


class IsPut(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method == 'PUT'


class IsPatch(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method == 'PATCH'


class IsDelete(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method == 'DELETE'


class IsOptions(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method == 'OPTIONS'


class IsHead(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method == 'HEAD'


class IsPhotoOwner(permissions.BasePermission):
    """Checks the ownership of the Photo instance
    From documentation: The instance-level has_object_permission method will only be called if the view-level has_permission checks have already passed.
    Also note that in order for the instance-level checks to run,
    the view code should explicitly call .check_object_permissions(request, obj)
    """

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_teacher:
            return obj.course.teacher == user.teacher
        else:
            return obj.student == user.student
