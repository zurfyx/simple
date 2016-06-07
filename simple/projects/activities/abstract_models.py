from django.db import models
from django.utils import timezone

from config import constants as globalConstants
from core.fields import RestrictedFile
from projects.abstract_models import AbstractTimeStamped
from projects.models import Project
from users.models import User


class AbstractProjectActivity(AbstractTimeStamped):
    """
    Project Activities for Students.
    Start_date & due_date represent the first and last date for users to hand
    in their Activity Replies.
    Allowed submissions represents the number of edits a user can do to their
    reply before their due date.
    """
    project = models.ForeignKey(Project)
    user = models.ForeignKey(User)
    title = models.CharField(max_length=200, unique=True)
    body = models.CharField(max_length=2000, blank=True, null=True)
    start_date = models.DateTimeField()
    due_date = models.DateTimeField()
    responses = models.ManyToManyField(User, through='ProjectActivityResponse',
                                       related_name='responded_activity')

    def is_closed(self):
        now = timezone.now()
        return now < self.start_date or now > self.due_date

    def __str__(self):
        return self.title

    class Meta:
        abstract = True
        verbose_name_plural = 'project activities'


class AbstractProjectActivityAttachment(models.Model):
    activity = models.ForeignKey('activities.ProjectActivity',
                                 related_name='activity_attachments')
    object = RestrictedFile(
        upload_to=globalConstants.MediaFile.PROJECT_ATTACHMENT.path,
        max_upload_size=globalConstants.MediaFile.PROJECT_ATTACHMENT.max_size,
        blank=True, null=True)

    class Meta:
        abstract = True


class AbstractProjectActivityResponse(AbstractTimeStamped):
    """
    Project Activity Response from User.
    """
    user = models.ForeignKey(User)
    activity = models.ForeignKey('ProjectActivity')
    body = models.CharField(max_length=20000)
    number_submissions = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.body

    class Meta:
        abstract = True
        unique_together = ('user', 'activity')


class AbstractProjectActivityResponseAttachment(models.Model):
    response = models.ForeignKey('activities.ProjectActivityResponse',
                                 related_name='activity_response_attachments')
    object = RestrictedFile(
        upload_to=globalConstants.MediaFile.PROJECT_ATTACHMENT.path,
        max_upload_size=globalConstants.MediaFile.PROJECT_ATTACHMENT.max_size,
        blank=True, null=True)

    class Meta:
        abstract = True
