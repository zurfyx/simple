from annoying.functions import get_object_or_None
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import UpdateView, CreateView

from core.mixins import OwnerRequiredMixin, CustomLoginRequiredMixin
from .models import Project, ProjectTechnicalRequest, ProjectRole
from . import constants


class ProjectRequiredMixin(object):
    """
    Checks if the project exists on the database. Otherwise, throws a 404.
    Project must be a URL pk parameter.
    """
    def dispatch(self, request, **kwargs):
        get_object_or_404(Project, id=kwargs['pk'])
        return super(ProjectRequiredMixin, self).dispatch(request, **kwargs)


class ApprovedProjectRequiredMixin(ProjectRequiredMixin):
    """
    Checks if the project exist on the database, and it has been previously
    approved. Otherwise, throws a 404.
    Project must be URL pk parameter.
    """
    def dispatch(self, request, *args, **kwargs):
        get_object_or_404(Project, id=kwargs['pk'], approved=True)
        return super(ApprovedProjectRequiredMixin, self).dispatch(request, **kwargs)


class ScientistRequiredMixin(CustomLoginRequiredMixin):
    """
    Either a Project Scientist or Administrator is required. Project has to be
    passed through a <video> or <pk> kwargs (<video> if <video> is not None else
    <pk>)
    Otherwise, it will return a 404 response.
    """
    def dispatch(self, request, **kwargs):
        user = request.user
        project = kwargs['video'] if 'video' in kwargs else kwargs['pk']

        if user.is_authenticated():
            project_role = \
                get_object_or_None(ProjectRole, user=user, project=project)
            scientist = constants.ProjectRoles.SCIENTIST
            if user.is_staff is False \
               and (project_role is None or project_role.role != scientist):
                raise Http404('Not a Scientist')
        return super(ScientistRequiredMixin, self).dispatch(request, **kwargs)


class ProjectEditMixin(OwnerRequiredMixin, ScientistRequiredMixin, UpdateView):
    model = Project

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.project = Project.objects.get(id=self.kwargs['pk'])
        return super(ProjectEditMixin, self).form_valid(form)


class ProjectQuestionMixin(OwnerRequiredMixin,CreateView):
    model = ProjectTechnicalRequest

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.project = Project.objects.get(id=self.kwargs['pk'])
        return super(ProjectEditMixin, self).form_valid(form)