from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.views.generic.edit import CreateView

from projects.activities.forms import ActivityNewForm
from projects.mixins import ScientistOrStudentRequiredMixin, \
    ScientistRequiredMixin
from projects.models import Project, ProjectRole
from .models import ProjectActivity


class ActivityList(ScientistOrStudentRequiredMixin, ListView):
    template_name = 'projects/activities/list.html'
    model = ProjectActivity
    context_object_name = 'activities'

    def get_context_data(self, **kwargs):
        context = super(ActivityList, self).get_context_data()
        context['project'] = get_object_or_404(Project, id=self.kwargs['project'])
        context['user_project_role'] = get_object_or_404(ProjectRole,
                                                         project=context['project'],
                                                         user=self.request.user)
        return context


class ActivityNewView(ScientistRequiredMixin, CreateView):
    template_name = 'projects/activities/new.html'
    model = ProjectActivity
    form_class = ActivityNewForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.project = Project.objects.get(id=self.kwargs['project'])
        return super(ActivityNewView, self).form_valid(form)

    def get_success_url(self):
        return reverse('projects:activities:list', args=[self.kwargs['project']])

    def get_context_data(self, **kwargs):
        context = super(ActivityNewView, self).get_context_data()
        context['project'] = get_object_or_404(Project, id=self.kwargs['project'])
        return context
