from django import forms

from projects.constants import ProjectRoles
from projects.models import Project, ProjectRole, ProjectTechnicalRequest


class ProjectRoleNewAdminForm(forms.ModelForm):
    """
    Form for creating a new Project on the admin panel
    """
    role = forms.ChoiceField(choices=ProjectRoles.PROJECT_ROLES)

    class Meta:
        model = ProjectRole
        fields = ('user', 'project', 'role', 'approved_role',)


class ProjectRoleEditAdminForm(forms.ModelForm):
    """
    Form for creating a new Project on the admin panel
    """
    role = forms.ChoiceField(choices=ProjectRoles.PROJECT_ROLES)

    class Meta:
        model = ProjectRole
        fields = ('user', 'project', 'role', 'approved_role',)
        readonly_fields = ('user', 'project',)


class ProjectNewForm(forms.ModelForm):
    """
    Form for creating a new Project
    """

    class Meta:
        model = Project
        fields = ('title', 'body', 'picture',)


class ProjectEditForm(forms.ModelForm):
    """
    Form for editing a Project
    """

    class Meta:
        model = Project
        fields = ('title', 'body', 'picture',)


class ProjectContributeForm(forms.ModelForm):
    """
    Form for requesting contribution to a Project
    """

    class Meta:
        model = ProjectRole
        fields = ('project', 'role')
        widgets = {'project': forms.HiddenInput()}

class ProjectQuestionForm(forms.ModelForm):
    """
    A form for editing comments.
    """

    class Meta:
        model = ProjectTechnicalRequest
        fields = ['question']