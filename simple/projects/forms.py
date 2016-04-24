from django import forms

from projects.models import Project


class ProjectNewForm(forms.ModelForm):
    """
    Form for creating a new Project
    """

    class Meta:
        model = Project
        fields = ('title', 'body',)
