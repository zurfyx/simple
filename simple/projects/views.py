from annoying.functions import get_object_or_None
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.views.generic.base import RedirectView, TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from core.mixins import CustomLoginRequiredMixin, HeadOfDepartmentMixin
from projects.forms import ProjectNewForm, ProjectContributeForm
from projects.mixins import ApprovedProjectRequiredMixin
from .models import Project, ProjectRole


class ProjectList(ListView):
    """
    Display list of projects
    """
    model = Project
    template_name = 'projects/list.html'
    context_object_name = 'projects'
    ordering = ['-created']


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
    success_url = 'projects:pending-approval'

    def form_valid(self, form):
        project = form.save(commit=False)
        project.owner = self.request.user
        project.save()
        messages.success(self.request, project.title)
        return HttpResponseRedirect(reverse(self.success_url))


class ProjectPendingApproval(TemplateView):
    template_name = 'projects/pending-approval.html'


class ProjectApproveList(HeadOfDepartmentMixin, ListView):
    model = Project
    template_name = 'projects/approve-list.html'
    context_object_name = 'projects'

    def get_queryset(self):
        return self.model.objects.filter(awaiting_approval=True)


class ProjectApproveDeny(HeadOfDepartmentMixin, RedirectView):
    pattern_name = 'projects:approve-list'
    approve = False

    def get_redirect_url(self, **kwargs):
        project = get_object_or_404(Project, pk=kwargs['pk'])
        project.awaiting_approval = False
        project.approved = self.approve
        project.save()
        return reverse(self.pattern_name)


class ProjectApproveView(ProjectApproveDeny):
    approve = True


class ProjectDenyView(ProjectApproveDeny):
    approve = False


class ProjectContributeView(CustomLoginRequiredMixin,
                            ApprovedProjectRequiredMixin, CreateView):
    template_name = 'projects/contribute.html'
    form_class = ProjectContributeForm
    success_url = 'projects:detail'

    def get_initial(self):
        return {
            'project': self.kwargs['pk'],
        }

    def form_valid(self, form):
        if self._previous_role_petition():
            url_contribute = reverse('projects:contribute',
                                     kwargs={'pk': self.kwargs['pk']})
            return HttpResponseRedirect(url_contribute)
        project_role = form.save(commit=False)
        project_role.user = self.request.user
        project_role.save()
        url_project = reverse(self.success_url,
                              kwargs={'pk': self.kwargs['pk']})
        return HttpResponseRedirect(url_project)

    def _previous_role_petition(self):
        """
        No duplicate role petitions per project can be recorded.
        Will return to the contribute view if so.
        """
        petition = ProjectRole.objects.get(user=self.request.user,
                                           project=self.kwargs['pk'])
        return petition is not None

    def get_context_data(self, **kwargs):
        context = super(ProjectContributeView, self).get_context_data(**kwargs)
        project = Project.objects.get(pk=self.kwargs['pk'])
        project_role = get_object_or_None(project.projectrole_set,
                                          user=self.request.user)
        context['project'] = project
        context['project_role'] = project_role
        return context
