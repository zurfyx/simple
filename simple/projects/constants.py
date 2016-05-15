class ProjectRoles(object):
    SCIENTIST = 1
    STUDENT = 2
    SCIENTIFIC_CITIZEN = 3

    PROJECT_ROLES = (
        (SCIENTIST, 'Scientist'),
        (STUDENT, 'Student'),
        (SCIENTIFIC_CITIZEN, 'Citizens Science'),
    )


class ProjectLogTypes(object):
    PROJECT_CREATE = 1
    PROJECT_EDIT = 2
    COMMENT_CREATE = 3
    COMMENT_EDIT = 4

    PROJECT_LOG_TYPES = (
        (PROJECT_CREATE, 'Project creation'),
        (PROJECT_EDIT, 'Project edition'),
        (COMMENT_CREATE, 'Comment addition'),
        (COMMENT_EDIT, 'Comment edition'),
    )


def project_constants(request):
    return {
        'PROJECT_ROLES': ProjectRoles,
        'PROJECT_LOG_TYPES': ProjectLogTypes,
    }
