from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    registration_number = models.CharField(_('identification'), max_length=11, unique=True, primary_key=True)
    email = models.EmailField(_('email address'))
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_teacher = models.BooleanField(_('is_teacher')) # if teacher True, if Student then False
    objects = UserManager()

    USERNAME_FIELD = 'registration_number'
    REQUIRED_FIELDS = ['is_teacher']

    def __str__(self):
        return "{}".format(self.registration_number)

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def is_staff(self):
        return self.is_superuser


# from django.contrib.auth import get_user_model
# User = get_user_model()
# u = User.objects.all()[0]
# u = User.objects.create_superuser(registration_number='16BCE0904', password='12ab34cd', is_teacher=True)