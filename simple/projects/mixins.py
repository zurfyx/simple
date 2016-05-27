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


class ProjectRoleRequiredMixin(CustomLoginRequiredMixin):
    """
    Either Project Role X or Administrator is required. Project has to be
    passed through a <video> or <pk> kwargs (<video> if <video> is not None else
    <pk>)
    Otherwise, it will return a 404 response.
    """
    project_roles_allowed = []  # i.e constants.ProjectRoles.SCIENTIST

    def _allowed_role(self, project_role):
        """
        Verifies is the user is allowed to interact with the project given
         a project role instance.
        """
        return False if project_role is None \
            else project_role.role in self.project_roles_allowed

    def dispatch(self, request, **kwargs):
        user = request.user
        project = kwargs['project'] if 'project' in kwargs else kwargs['pk']
        project_obj = get_object_or_404(Project, id=project)

        if user.is_authenticated():
            project_role = \
                get_object_or_None(ProjectRole, user=user, project=project_obj)
            if not (user.is_staff or self._allowed_role(project_role)):
                raise Http404('Not a Scientist')
        return super(ProjectRoleRequiredMixin, self).dispatch(request, **kwargs)


class ScientistRequiredMixin(ProjectRoleRequiredMixin):
    """
    Either a Project Scientist or Administrator is required.
    """
    project_roles_allowed = [constants.ProjectRoles.SCIENTIST]


class StudentRequiredMixin(ProjectRoleRequiredMixin):
    """
    Either a Student or Administrator is required
    """
    project_roles_allowed = [constants.ProjectRoles.STUDENT]


class ScientistOrStudentRequiredMixin(ProjectRoleRequiredMixin):
    """
    Either a Scientist or Student or Administrator is required
    """
    project_roles_allowed = [
        constants.ProjectRoles.SCIENTIST,
        constants.ProjectRoles.STUDENT,
    ]


class ProjectEditMixin(ScientistRequiredMixin, UpdateView):
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