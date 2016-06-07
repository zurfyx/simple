from django import forms
from multiupload.fields import MultiFileField

from config.constants import MediaFile
from .models import Comment


class CommentAddForm(forms.ModelForm):
    """
    A form for creating comments.
    """
    attachments = MultiFileField(required=False, min_num=1,
                                 max_num=MediaFile.PROJECT_ATTACHMENT_MULTIUPLOAD,
                                 max_file_size=MediaFile.PROJECT_ATTACHMENT.max_size)

    class Meta:
        model = Comment
        fields = ('content',)


class CommentEditForm(forms.ModelForm):
    """
    A form for editing comments.
    """
    attachments = MultiFileField(required=False, min_num=1,
                                 max_num=MediaFile.PROJECT_ATTACHMENT_MULTIUPLOAD,
                                 max_file_size=MediaFile.PROJECT_ATTACHMENT.max_size)

    class Meta:
        model = Comment
        fields = ('content',)
