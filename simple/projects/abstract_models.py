from django.db import models

from projects.constants import ProjectRoles
from users.models import User


class AbstractTimeStamped(models.Model):
    """
    Auto-updated created and modified fields
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AbstractProject(AbstractTimeStamped):
    """
    Defines a Project Model.
    """
    owner = models.ForeignKey(User)
    title = models.CharField(max_length=200, unique=True)
    body = models.CharField(max_length=20000)
    roles = models.ManyToManyField(User, through='ProjectRole',
                                   related_name='projects')
    awaiting_approval = models.BooleanField(default=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return '{0}'.format(self.title)

    class Meta:
        abstract = True


class AbstractProjectRole(models.Model):
    """
    Special user roles for projects.
    These can be 1 => Scientist, 2 => Student, 3 => Scientific Citizen
    (check constants).
    Project owner will always be a scientist.
    """
    user = models.ForeignKey(User)
    project = models.ForeignKey('Project')
    role = models.PositiveIntegerField(default=1,
                                       choices=ProjectRoles.PROJECT_ROLES)
    approved_role = models.BooleanField(default=False)

    def __str__(self):
        return ProjectRoles.PROJECT_ROLES[self.role][1]

    class Meta:
        abstract = True
        unique_together = ('user', 'project')
