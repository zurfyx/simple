from .abstract_models import AbstractProjectActivity, \
    AbstractProjectActivityResponse, AbstractProjectActivityAttachment, \
    AbstractProjectActivityResponseAttachment


class ProjectActivity(AbstractProjectActivity):
    pass


class ProjectActivityAttachment(AbstractProjectActivityAttachment):
    pass


class ProjectActivityResponse(AbstractProjectActivityResponse):
    pass


class ProjectActivityResponseAttachment(AbstractProjectActivityResponseAttachment):
    pass
