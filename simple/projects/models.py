from __future__ import unicode_literals

from .abstract_models import AbstractProject, AbstractProjectRole, \
    AbstractProjectRating, AbstractProjectLog, AbstractProjectTechnicalRequest, \
    AbstractProjectFavorite


class Project(AbstractProject):
    pass


class ProjectRole(AbstractProjectRole):
    pass


class ProjectRating(AbstractProjectRating):
    pass


class ProjectFavorite(AbstractProjectFavorite):
    pass


class ProjectLog(AbstractProjectLog):
    pass


class ProjectTechnicalRequest(AbstractProjectTechnicalRequest):
    pass
