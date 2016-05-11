from django.forms import ModelForm

from projects.comments.models import *


class CommentAddForm(ModelForm):
    """
    A form for creating comments.
    """

    class Meta:
        model = Comment
        fields = ['content']


class CommentEditForm(ModelForm):
    """
    A form for editing comments.
    """

    class Meta:
        model = Comment
        fields = ['content']
