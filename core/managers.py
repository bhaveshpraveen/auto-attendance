from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, registration_number, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not registration_number:
            raise ValueError('The given registration number must be set')
        user = self.model(registration_number=registration_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, registration_number, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(registration_number, password, **extra_fields)

    def create_superuser(self, registration_number, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(registration_number, password, **extra_fields)

# 12ab34cd
# https://stackoverflow.com/questions/41612654/createsuperuser-didnt-ask-for-username#41612846