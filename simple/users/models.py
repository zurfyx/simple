from __future__ import unicode_literals

from .abstract_models import AbstractUser, AbstractUserLog


class User(AbstractUser):
    pass


class UserLog(AbstractUserLog):
    pass
