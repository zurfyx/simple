from django.db import models

from users.models import User


class AbstractProject(models.Model):
    """
    Defines a Project Model.
    """
    owner = models.ForeignKey(User)
    title = models.CharField(max_length=200)
    body = models.CharField(max_length=20000)
    roles = models.ManyToManyField(User, through='ProjectRole',
                                   related_name='projects')
    approved = models.BooleanField(default=False)

    def __str__(self):
        return '{0}'.format(self.title)

    class Meta:
        abstract = True


class AbstractProjectRole(models.Model):
    """
    Special user roles for projects.
    These can be 1 => Scientist, 2 => Student, 3 => Scientific Citizen.
    Project owner will always be a scientist.
    """
    user = models.ForeignKey(User)
    project = models.ForeignKey('Project')
    role = models.PositiveIntegerField(default=1)
    approved_role = models.BooleanField(default=False)

    def __str__(self):
        return str(self.role)

    class Meta:
        abstract = True
