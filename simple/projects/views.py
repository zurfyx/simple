from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from core.mixins import CustomLoginRequiredMixin
from projects.forms import ProjectNewForm
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


class ProjectNewView(CustomLoginRequiredMixin, CreateView):
    template_name = 'projects/new.html'
    form_class = ProjectNewForm
    success_url = 'projects:list'

    def form_valid(self, form):
        project = form.save(commit=False)
        project.owner = self.request.user
        project.save()
        return HttpResponseRedirect(reverse(self.success_url))
