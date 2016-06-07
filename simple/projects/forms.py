from django import forms
from multiupload.fields import MultiFileField

from config.constants import MediaFile
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
    attachments = MultiFileField(required=False, min_num=1, max_num=10,
                                 max_file_size=MediaFile.PROJECT_ATTACHMENT.max_size)

    class Meta:
        model = Project
        fields = ('title', 'body', 'picture',)


class ProjectEditForm(forms.ModelForm):
    """
    Form for editing a Project
    """
    attachments = MultiFileField(required=False, min_num=1, max_num=10,
                                 max_file_size=MediaFile.PROJECT_ATTACHMENT.max_size)

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
    A form for add questions.
    """

    class Meta:
        model = ProjectTechnicalRequest
        fields = ['question','to_user']


class ProjectAnswerForm(forms.ModelForm):
    """
    A form for add answers.
    """

    class Meta:
        model = ProjectTechnicalRequest
        fields = ['answer']
