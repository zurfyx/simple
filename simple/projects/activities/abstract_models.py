from django.db import models

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
    allowed_submissions = models.PositiveIntegerField(default=1)
    responses = models.ManyToManyField(User, through='ProjectActivityResponse',
                                       related_name='responded_activity')

    def __str__(self):
        return self.title

    class Meta:
        abstract = True
        verbose_name_plural = 'project activities'


class AbstractProjectActivityResponse(AbstractTimeStamped):
    """
    Project Activity Response from User.
    """
    user = models.ForeignKey(User)
    activity = models.ForeignKey('ProjectActivity')
    body = models.CharField(max_length=20000)
    number_submissions = models.PositiveIntegerField(default=0)

    def response(self, body):
        self.body = body
        self.number_submissions += 1

    def __str__(self):
        return self.body

    class Meta:
        abstract = True
        unique_together = ('user', 'activity')
