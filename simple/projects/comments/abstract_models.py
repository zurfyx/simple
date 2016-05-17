from django.db import models

from users.models import User
from projects.abstract_models import AbstractTimeStamped


class AbstractComment(AbstractTimeStamped):
    """
    Representation of the Project Comment (feedback).
    """
    user = models.ForeignKey(User)
    project = models.ForeignKey('projects.Project', related_name='comments')
    content = models.CharField(max_length=10000)
    is_removed = models.BooleanField(default=False)

    def __str__(self):
        return self.content if self.content < 50 else self.content[:50] + '...'

    class Meta:
        abstract = True
