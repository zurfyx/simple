ACTIVE_DAYS = 30  # up to X days a user is considered active


class UserRoles(object):
    MEMBER = 1
    MODERATOR = 2
    HEAD_OF_DEPARTMENT = 3

    USER_ROLES = (
        (MEMBER, 'Member'),
        (MODERATOR, 'Moderator'),
        (HEAD_OF_DEPARTMENT, 'Head of Department')
    )
