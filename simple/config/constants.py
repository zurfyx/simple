PROJECT_NAME = 'Simple'


class MediaFile(object):
    class File(object):
        def __init__(self, path, max_size):
            self.path = path
            self.max_size = max_size

    USER_AVATAR = File('users/avatar', 2 * 1024 * 1024)  # 2 MB
    PROJECT_PICTURE = File('projects/picture', 2 * 1024 * 1024)
    PROJECT_ATTACHMENT = File('projects/attachment', 20 * 1024 * 1024)


def app_constants(request):
    return {
        'PROJECT_NAME': PROJECT_NAME,
    }
