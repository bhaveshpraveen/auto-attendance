from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


User = settings.AUTH_USER_MODEL


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher')

    def __str__(self):
        return "%s" % self.user.registration_number


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student')
    teachers = models.ManyToManyField('Teacher', related_name='students')
    courses = models.ManyToManyField('Course', related_name='students')

    def __str__(self):
        return "%s" % self.user.registration_number


class Course(models.Model):
    SJT = 'sjt'
    TT = 'tt'
    GDN = 'gdn'
    SMV = 'smv'
    VENUE_CHOICES = (
        (SJT, SJT),
        (TT, TT),
        (GDN, GDN),
        (SMV, SMV),
    )
    course_code = models.CharField(max_length=20)
    course_name = models.CharField(max_length=100)
    slot = models.CharField(max_length=20)
    room = models.CharField(max_length=4, choices=VENUE_CHOICES, default=SJT)
    teacher = models.ForeignKey(Teacher, related_name='courses', on_delete=models.CASCADE)

    def __str__(self):
        return "{} {} {}".format(self.course_name, self.slot, self.room)

    class Meta:
        unique_together = (
            ('course_code', 'slot', 'teacher'),
        )


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>

    return 'user_{0}/{1}'.format(instance.user.id, filename)


class Photo(models.Model):
    img = models.ImageField(upload_to='files/')
    identification = models.CharField(max_length=100, unique=True)
    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='photos', null=True, blank=True)
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='photos', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s" % self.identification


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_teacher:
            Teacher.objects.create(user=instance)
        else:
            Student.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if instance.is_teacher:
        instance.teacher.save()
    else:
        instance.student.save()


# https://stackoverflow.com/questions/18676156/how-to-properly-use-the-choices-field-option-in-django#32657683