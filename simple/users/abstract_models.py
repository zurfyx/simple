import datetime

from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.utils.timezone import utc
from django.core.urlresolvers import reverse
from config import constants as globalConstants
from users.constants import UserLogTypes
from .managers import EmailUserManager
from . import constants


class AbstractUser(AbstractBaseUser):
    """
    Defines User Custom Model.
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
    avatar = models.ImageField(upload_to=globalConstants.FilePath.USER_AVATAR,
                               blank=True, null=True)

    # analytics
    views = models.PositiveIntegerField(default=0)

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
        return u'{0} {1}'.format(self.first_name, self.last_name)

    def get_short_name(self):
        return self.first_name

    def get_age(self):
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        if self.birthday is None or self.birthday == '':
            return None
        return dir(now - self.birthday)

    def get_role_str(self):
        return constants.UserRoles.USER_ROLES[self.role-1][1]

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    
    def get_absolute_url(self):
        return reverse('users:account', kwargs={'pk':self.pk})

    def __str__(self):
        return '{0}'.format(self.email)

    class Meta:
        abstract = True


class AbstractUserLog(models.Model):
    """
    Project log (saves all occurred events in a project).
    type = i.e. 'ACTIVITY_AVAILABLE' (see user constants)
    description = text description of the event
    reference = <id> of the type
    """
    user = models.ForeignKey('User')
    type = models.IntegerField(choices=UserLogTypes.USER_LOG_TYPES)
    description = models.CharField(max_length=500, blank=True, null=True)
    reference = models.CharField(max_length=255, blank=True, null=True)

    def get_type_str(self):
        return UserLogTypes.USER_LOG_TYPES[self.type][1]

    def __str__(self):
        return '({0}, {1}) -> {2}' \
            .format(self.user, self.project,
                    UserLogTypes.USER_LOG_TYPES[self.type][1])

    class Meta:
        abstract = True
