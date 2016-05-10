from django import forms
from models import *
from django.forms import ModelForm


class CommendAddForm(ModelForm):
    """
    A form for creating comments.
    """

    class Meta:
        model = Comment
        fields = ['content']
