from django.db import models
from django.core.urlresolvers import reverse
from config import constants as globalConstants
from users.models import User
from .constants import ProjectRoles, ProjectLogTypes


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
    user = models.ForeignKey(User)
    title = models.CharField(max_length=200, unique=True)
    body = models.CharField(max_length=20000)
    language = models.CharField(max_length=50, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    picture = models.ImageField(upload_to=globalConstants.FilePath.PROJECT_PICTURE,
                                blank=True, null=True)

    # Roles
    roles = models.ManyToManyField(User, through='ProjectRole',
                                   related_name='enrolled_projects')
    awaiting_approval = models.BooleanField(default=True)
    approved = models.BooleanField(default=False)

    # Rating
    ratings = models.ManyToManyField(User, through='ProjectRating',
                                     related_name='rated_projects')
    upvotes = models.PositiveIntegerField(default=0)
    downvotes = models.PositiveIntegerField(default=0)

    # Analytics
    visits = models.PositiveIntegerField(default=0)
    unique_visits = models.PositiveIntegerField(default=0)

    def __str__(self):
        return '{0}'.format(self.title)

    def get_absolute_url(self):
        return reverse('projects:user-list', kwargs={'user':self.pk})

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

    def get_role_str(self):
        return ProjectRoles.PROJECT_ROLES[self.role][1]

    def __str__(self):
        return '({0}, {1}) -> {2}'\
            .format(self.user, self.project, ProjectRoles.PROJECT_ROLES[self.role][1])

    class Meta:
        abstract = True
        unique_together = ('user', 'project')


class AbstractProjectRating(models.Model):
    """
    Project rating (either upvote or downvote).
    Use the upvote() downvote() methods to set the rate.
    Internally, a positive vote will have rating == True, else rating == False.
    If the user has not voted on the project, this model will not exist.
    """
    user = models.ForeignKey(User)
    project = models.ForeignKey('Project')
    rate_date = models.DateTimeField(auto_now=True)
    rating = models.BooleanField()

    def upvote(self):
        self.rating = True

    def downvote(self):
        self.rating = False

    class Meta:
        abstract = True
        unique_together = ('user', 'project')


class AbstractProjectLog(models.Model):
    """
    Project log (saves all occurred events in a project).
    type = i.e. 'COMMENT_CREATE' (see project constants)
    description = text description of the event
    reference = <id> of the type
    """
    project = models.ForeignKey('Project')
    type = models.IntegerField(choices=ProjectLogTypes.PROJECT_LOG_TYPES)
    description = models.CharField(max_length=500, blank=True, null=True)
    reference = models.CharField(max_length=255, blank=True, null=True)

    def get_type_str(self):
        return ProjectLogTypes.PROJECT_LOG_TYPES[self.type][1]

    def __str__(self):
        return '({0}, {1}) -> {2}' \
            .format(self.user, self.project,
                    ProjectLogTypes.PROJECT_LOG_TYPES[self.type][1])

    class Meta:
        abstract = True


class AbstractProjectTechnicalRequest(models.Model):
    """
    Project Technical Requests or QA to citizens science members.
    Use reply(<answer>) method to save a reply to a technical request.
    """
    project = models.ForeignKey('Project')
    from_user = models.ForeignKey(User, related_name='technical_request_from_user')
    to_user = models.ForeignKey(User, related_name='technical_request_to_user')
    created = models.DateTimeField(auto_now_add=True)
    question = models.CharField(max_length=200)
    answer = models.CharField(max_length=20000)
    replied = models.BooleanField(default=False)

    def reply(self, answer):
        self.answer = answer
        self.replied = True

    class Meta:
        abstract = True


class AbstractProjectActivity(AbstractTimeStamped):
    """
    Project Activities for Students.
    Start_date & due_date represent the first and last date for users to hand
    in their Activity Replies.
    Allowed submissions represents the number of edits a user can do to their
    reply before their due date.
    """
    project = models.ForeignKey('Project')
    user = models.ForeignKey(User)
    title = models.CharField(max_length=200)
    body = models.CharField(max_length=2000, blank=True, null=True)
    start_date = models.DateTimeField()
    due_date = models.DateTimeField()
    allowed_submissions = models.PositiveIntegerField(default=1)
    responses = models.ManyToManyField(User, through='ProjectActivityResponse',
                                       related_name='responded_activity')

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

    class Meta:
        abstract = True
        unique_together = ('user', 'activity')
