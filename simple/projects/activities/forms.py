from datetimewidget.widgets import DateTimeWidget
from django import forms

from .models import ProjectActivity


class ActivityNewForm(forms.ModelForm):
    """
    Form for creating a new Activity
    """

    class Meta:
        model = ProjectActivity
        fields = ('title', 'body', 'start_date', 'due_date',
                  'allowed_submissions')
        widgets = {
            'body': forms.Textarea(attrs={'placeholder': u'Activity description'}),
            'start_date': DateTimeWidget(),
            'due_date': DateTimeWidget(),
        }
