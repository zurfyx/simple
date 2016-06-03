from annoying.functions import get_object_or_None
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from projects.activities.forms import ActivityNewForm, ActivityResponseNewForm
from projects.activities.mixins import ActivityOpenMixin
from projects.mixins import ScientistOrStudentRequiredMixin, \
    ScientistRequiredMixin, StudentRequiredMixin
from projects.models import Project, ProjectRole
from .models import ProjectActivity, ProjectActivityResponse


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
        form.instance.project = get_object_or_404(Project, id=self.kwargs['project'])
        return super(ActivityNewView, self).form_valid(form)

    def get_success_url(self):
        return reverse('projects:activities:list', args=[self.kwargs['project']])

    def get_context_data(self, **kwargs):
        context = super(ActivityNewView, self).get_context_data()
        context['project'] = get_object_or_404(Project, id=self.kwargs['project'])
        return context


class ActivityDetailView(DetailView):
    template_name = 'projects/activities/detail.html'
    model = ProjectActivity
    context_object_name = 'activity'

    def get_context_data(self, **kwargs):
        context = super(ActivityDetailView, self).get_context_data()
        context['project'] = get_object_or_404(Project, id=self.kwargs['project'])
        context['activity_responses'] = context['activity']\
            .projectactivityresponse_set.all()
        context['user_activity_responses'] = context['activity']\
            .projectactivityresponse_set.filter(user=self.request.user)
        return context

#
# ACTIVITY REPLIES
#


class ActivityResponseNewView(StudentRequiredMixin, ActivityOpenMixin,
                              CreateView):
    template_name = "projects/activities/response-new.html"
    model = ProjectActivityResponse
    form_class = ActivityResponseNewForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.project = get_object_or_404(Project, id=self.kwargs['project'])
        form.instance.activity = get_object_or_404(ProjectActivity,
                                                   id=self.kwargs['activity'])
        return super(ActivityResponseNewView, self).form_valid(form)

    def get_success_url(self):
        return reverse('projects:activities:list',
                       args=[self.kwargs['project']])

    def get_context_data(self, **kwargs):
        context = super(ActivityResponseNewView, self).get_context_data(**kwargs)
        context['project'] = get_object_or_404(Project, id=self.kwargs['project'])
        context['activity'] = get_object_or_404(ProjectActivity,
                                                id=self.kwargs['activity'])
        context['activity_response'] = \
            get_object_or_None(ProjectActivityResponse,
                               user=self.request.user,
                               activity=self.kwargs['project'])
        return context
