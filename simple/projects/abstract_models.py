from django.db import models

from users.models import User


class AbstractProject(models.Model):
    """
    Remember that owner is inherited from User.
    """
    owner = models.ForeignKey(User)
    title = models.CharField(max_length=200)
    body = models.CharField(max_length=20000)
    #roles = models.ManyToManyField(User, through='User')
    approved = models.BooleanField(default=False)

    def __unicode__(self):
        return str(self.owner)

    class Meta:
        abstract = True


class AbstractProjectRoles(AbstractProject):
    """
    Defining role and approved projects.
    """
    role = models.PositiveIntegerField(default=1)
    approved_role = models.BooleanField(default=False)

    def __str__(self):
        return str(self.role)

    class Meta:
        abstract = True
