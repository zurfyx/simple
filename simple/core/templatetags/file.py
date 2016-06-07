import os

from django import template

register = template.Library()


@register.filter
def filename(value):
    return os.path.basename(value.file.name)


@register.filter
def filesize(bytes):
    values = (
        (1024 * 1024 * 1024 * 1024, 'TB'),
        (1024 * 1024 * 1024, 'GB'),
        (1024 * 1024, 'MB'),
        (1024, 'KB'),
        (1, 'Bytes')
    )

    for value in values:
        operation = bytes / value[0]
        if operation > 0:
            return '{0} {1}'.format(operation, value[1])
    return 0
