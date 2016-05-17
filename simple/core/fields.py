from django import forms
from django.db.models import ImageField, FileField
from django.template.defaultfilters import filesizeformat


class ContentTypeRestrictedFileField(FileField):
    """
    Optional type and size restriction of a FileField.
    Extend me like:
        RestrictedMyField(ContentTypeRestrictedFileField)
        RestrictedMyImageField(ImageFile, ContentTypeRestrictedFileField)
    Usage in models:
        RestrictedMyField(content_types=[...], max_upload_size=1000)
    You can specify:
        * content_types - list containing allowed content_types. Example: ['application/pdf', 'image/jpeg']
        * max_upload_size - a number indicating the maximum file size allowed for upload.
            2.5MB - 2621440
            5MB - 5242880
            10MB - 10485760
            20MB - 20971520
            50MB - 5242880
            100MB 104857600
            250MB - 214958080
            500MB - 429916160
    http://stackoverflow.com/a/9016664/2034015
    """
    content_types = None
    max_upload_size = None

    def __init__(self, *args, **kwargs):
        if 'content_types' in kwargs:
            self.content_types = kwargs.pop("content_types")
        if 'max_upload_size' in kwargs:
            self.max_upload_size = kwargs.pop("max_upload_size")

        super(ContentTypeRestrictedFileField, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        data = super(ContentTypeRestrictedFileField, self).clean(*args, **kwargs)

        file = data.file
        try:
            content_type = file.content_type
            if self.content_types and content_type not in self.content_types:
                raise forms.ValidationError('Filetype not supported.')
            if self.max_upload_size and file._size > self.max_upload_size:
                raise forms.ValidationError(u'Maximum file size is {0}'
                                            .format(filesizeformat(self.max_upload_size)))
        except AttributeError:
            pass

        return data


class RestrictedFile(ContentTypeRestrictedFileField):
    pass


class RestrictedImageField(ImageField, ContentTypeRestrictedFileField):
    """
    A ContentTypeRestrictedFileField specifically for images; allowed formats
    are already set by default.
    """
    content_types = ['image/jpeg', 'image/png', 'image/gif']


class RestrictedNonAnimatedImageField(RestrictedImageField):
    """
    A RestrictedImageField that does not allow animated images (.gif).
    """
    content_types = ['image/jpeg', 'image/png']


class RestrictedVideoField(RestrictedFile):
    """
    A ContentTypeRestrictedFileField specifically for videos; allowed formats
    are already set by default.
    """
    content_types = ['video/x-flv']
