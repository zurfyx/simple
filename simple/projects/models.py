from __future__ import unicode_literals

from .abstract_models import AbstractProject, AbstractProjectRole, \
    AbstractProjectRating, AbstractProjectLog, AbstractProjectTechnicalRequest, \
    AbstractProjectActivity, AbstractProjectActivityResponse, \
    AbstractProjectComment


class Project(AbstractProject):
    pass


class ProjectComment(AbstractProjectComment):
    pass


class ProjectRole(AbstractProjectRole):
    pass


class ProjectRating(AbstractProjectRating):
    pass


class ProjectLog(AbstractProjectLog):
    pass


class ProjectTechnicalRequest(AbstractProjectTechnicalRequest):
    pass


class ProjectActivity(AbstractProjectActivity):
    pass


class ProjectActivityResponse(AbstractProjectActivityResponse):
    pass
