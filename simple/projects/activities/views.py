from django.views.generic import ListView
from django.views.generic.edit import CreateView

from .models import ProjectActivity


class ActivityList(ListView):
    # TODO student required mixin
    template_name = 'projects/activities/list.html'
    model = ProjectActivity
    context_object_name = 'activities'


class ActivityNewView(CreateView):
    model = ProjectActivity
