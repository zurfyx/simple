from django.db import models
from config import constants as globalConstants
from core.fields import RestrictedNonAnimatedImageField
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
    picture = RestrictedNonAnimatedImageField(
        upload_to=globalConstants.MediaFile.PROJECT_PICTURE.path,
        max_upload_size=globalConstants.MediaFile.PROJECT_PICTURE.max_size,
        blank=True, null=True)

    # Roles
    roles = models.ManyToManyField(User, through='ProjectRole',
                                   related_name='enrolled_projects')
    awaiting_approval = models.BooleanField(default=True)
    approved = models.BooleanField(default=False)

    # Rating
    ratings = models.ManyToManyField(User, through='ProjectRating',
                                     related_name='rates_projects')
    upvotes = models.PositiveIntegerField(default=0)
    downvotes = models.PositiveIntegerField(default=0)

    # Favorites
    favorites = models.ManyToManyField(User, through='ProjectFavorite',
                                       related_name='favorites_projects')

    # Analytics
    visits = models.PositiveIntegerField(default=0)
    unique_visits = models.PositiveIntegerField(default=0)

    def __str__(self):
        return '{0}'.format(self.title)

    class Meta:
        abstract = True

    def increase_visits(self):
        self.visits += 1
        self.save()


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
        return ProjectRoles.PROJECT_ROLES[self.role-1][1]

    def __str__(self):
        return '({0}, {1}) -> {2}'\
            .format(self.user, self.project, ProjectRoles.PROJECT_ROLES[self.role-1][1])

    class Meta:
        abstract = True
        unique_together = ('user', 'project')


class AbstractProjectRating(AbstractTimeStamped):
    """
    Project rating (either upvote or downvote).
    Use the upvote() downvote() methods to set the rate, is_upvoted()
    is_downvoted() to get the current rate.
    Internally, a positive vote will have rating == True, else rating == False.
    If the user has not voted on the project, this model will not exist.
    """
    user = models.ForeignKey(User)
    project = models.ForeignKey('Project')
    rating = models.BooleanField()

    def is_upvoted(self):
        return self.rating

    def is_downvoted(self):
        return not self.rating

    def upvote(self):
        self.rating = True

    def downvote(self):
        self.rating = False

    class Meta:
        abstract = True
        unique_together = ('user', 'project')


class AbstractProjectFavorite(AbstractTimeStamped):
    """
    Project favourite by an User
    """
    user = models.ForeignKey(User)
    project = models.ForeignKey('Project')

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
