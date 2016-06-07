from django.db import models

from config import constants as globalConstants
from core.fields import RestrictedFile
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


class AbstractCommentAttachment(models.Model):
    comment = models.ForeignKey('comments.Comment',
                                related_name='comment_attachments')
    object = RestrictedFile(
        upload_to=globalConstants.MediaFile.PROJECT_ATTACHMENT.path,
        max_upload_size=globalConstants.MediaFile.PROJECT_ATTACHMENT.max_size,
        blank=True, null=True)

    class Meta:
        abstract = True
