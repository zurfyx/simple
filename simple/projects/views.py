from django.views.generic import ListView
from django.views.generic.detail import DetailView

from .models import Project


class ProjectList(ListView):
    """
    Display list of projects
    """
    model = Project
    template_name = 'projects/list.html'
    context_object_name = 'projects'


class ProjectDetail(DetailView):
    """
    Display project details
    """
    model = Project
    template_name = 'projects/detail.html'
    context_object_name = 'project'
