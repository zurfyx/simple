PROJECT_NAME = 'Simple'


class FilePath(object):
    USER_AVATAR = '/uploads/avatar/'
    PROJECT_PICTURE = '/uploads/project/picture'
    PROJECT_DOCUMENTATION = '/uploads/project/documentation'


def app_constants(request):
    return {
        'PROJECT_NAME': PROJECT_NAME,
    }
