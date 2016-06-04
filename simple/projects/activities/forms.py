from datetimewidget.widgets import DateTimeWidget
from django import forms

from .models import ProjectActivity, ProjectActivityResponse


class ActivityNewForm(forms.ModelForm):
    """
    Form for creating a new Activity
    """

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

    class Meta:
        model = ProjectActivityResponse
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={'placeholder': u'Response description'})
        }
