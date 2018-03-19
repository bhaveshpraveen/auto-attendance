from django.contrib import admin

from .models import Course, Teacher, Photo, Student

admin.site.register(Course)
admin.site.register(Teacher)
admin.site.register(Photo)
admin.site.register(Student)

