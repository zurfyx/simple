from django import forms
from models import *
from django.forms import ModelForm


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
