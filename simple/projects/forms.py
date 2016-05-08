from django import forms
from django.db import models

from projects.constants import ProjectRoles
from projects.models import Project, ProjectRole


class ProjectNewForm(forms.ModelForm):
    """
    Form for creating a new Project
    """

    class Meta:
        model = Project
        fields = ('title', 'body',)


class ProjectContributeForm(forms.ModelForm):
    """
    Form for requesting contribution to a Project
    """

    class Meta:
        model = ProjectRole
        fields = ('project', 'role')
        widgets = {'project': forms.HiddenInput()}
