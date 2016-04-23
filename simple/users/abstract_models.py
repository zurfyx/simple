import datetime

from django.contrib.auth.base_user import AbstractBaseUser
from .managers import EmailUserManager
from django.db import models
from django.utils.timezone import utc

from . import constants


class AbstractUser(AbstractBaseUser):
    """
    Remember that password and last_login are inherited from AbstractBaseUser.
    """
    email = models.EmailField(db_index=True, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=300)
    last_name = models.CharField(max_length=300)
    birthday = models.DateTimeField(null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    occupation = models.CharField(max_length=100, null=True, blank=True)
    role = models.PositiveIntegerField(default=1)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = EmailUserManager()

    @property
    def is_active(self):
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        last_seen = self.date_joined if self.last_login is None else \
            max(self.date_joined, self.last_login)
        return (now - last_seen).days <= constants.ACTIVE_DAYS

    @property
    def is_superuser(self):
        return self.is_staff

    def get_full_name(self):
        return '{0} {1}'.format(self.first_name, self.last_name)

    def get_short_name(self):
        return self.first_name

    def get_age(self):
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        if self.birthday is None or self.birthday == '':
            return None
        return dir(now - self.birthday)

    def get_role_str(self):
        role = [
            (1, 'Member'),
            (2, 'Head of Department'),
            (3, 'Moderator'),
        ]
        return role[self.role]

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def __unicode__(self):
        return '{0}'.format(self.email)

    class Meta:
        abstract = True
