from datetimewidget.widgets import DateTimeWidget
from django import forms
from multiupload.fields import MultiFileField

from config.constants import MediaFile
from .models import ProjectActivity, ProjectActivityResponse


class ActivityNewForm(forms.ModelForm):
    """
    Form for creating a new Activity
    """
    attachments = MultiFileField(required=False, min_num=1,
                                 max_num=MediaFile.PROJECT_ATTACHMENT_MULTIUPLOAD,
                                 max_file_size=MediaFile.PROJECT_ATTACHMENT.max_size)

    class Meta:
        model = ProjectActivity
        fields = ('title', 'body', 'start_date', 'due_date')
        widgets = {
            'body': forms.Textarea(attrs={'placeholder': u'Activity description'}),
            'start_date': DateTimeWidget(),
            'due_date': DateTimeWidget(),
        }


class ActivityResponseNewForm(forms.ModelForm):
    """
    Form for replying to an Activity
    """
    attachments = MultiFileField(required=False, min_num=1,
                                 max_num=MediaFile.PROJECT_ATTACHMENT_MULTIUPLOAD,
                                 max_file_size=MediaFile.PROJECT_ATTACHMENT.max_size)

    class Meta:
        model = ProjectActivityResponse
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={'placeholder': u'Response description'})
        }
