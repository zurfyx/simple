from annoying.functions import get_object_or_None
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.views.generic.base import RedirectView, TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from core.mixins import CustomLoginRequiredMixin, HeadOfDepartmentMixin
from projects.forms import ProjectNewForm, ProjectContributeForm
from projects.mixins import ApprovedProjectRequiredMixin
from users.models import User
from .models import Project, ProjectRole


class ProjectList(ListView):
    """
    Display list of projects.
    If a project is unapproved, it will only be returned to HeadOfDepartment.
    """
    model = Project
    template_name = 'projects/list.html'
    context_object_name = 'projects'
    ordering = ['-created']


class UserProjectList(ProjectList):
    """
    Displays a list of user projects, by filtering the project current list.
    """
    # TODO If any project is unapproved, it will only be visible to
    # HeadOfDepartment
    template_name = 'projects/user-list.html'

    def get_queryset(self):
        return self.model.objects.filter(owner=self.kwargs['user'])


class ProjectDetail(DetailView):
    """
    Display project details.
    If a project is unapproved, it will only be returned to HeadOfDepartment. A
    404 messages will be thrown otherwise.
    """
    # TODO If unapproved, only visible to HeadOfDepartment.
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
    """
    Basic view to display that a project is "now pending to be approved".
    """
    template_name = 'projects/pending-approval.html'


class ProjectApproveList(HeadOfDepartmentMixin, ListView):
    """
    Displays a list of projects pending to be approved. Only accessible through
    a HeadOfDepartment account.
    """
    model = Project
    template_name = 'projects/approve-list.html'
    context_object_name = 'projects'

    def get_queryset(self):
        return self.model.objects.filter(awaiting_approval=True)


class ProjectApproveDeny(HeadOfDepartmentMixin, RedirectView):
    """
    Generic redirect view to handle the action approve / deny, which can only
    be accessed through a HeadOfDepartment account.
    """
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
    """
    Form through which any logged in user can request to participate in an
     approved project.
    If the project has already received a petition from the user, and it is
     still pending to be reviewed it will ignore the petition.
    """
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
        petition = get_object_or_None(ProjectRole, user=self.request.user,
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


class ProjectApproveContributionList(CustomLoginRequiredMixin, UserProjectList):
    """
    Displays a list of current logged in user projects, that have users who
    are pending a contribution approval.
    """
    template_name = 'projects/approve-contribution-list.html'
    context_object_name = 'projectroles'

    def get_queryset(self):
        # retrieve projects from the logged in user
        self.kwargs['user'] = self.request.user
        user_projects = super(ProjectApproveContributionList, self).get_queryset()

        # set up filters for an OR unique query by projects and not approved yet
        filters = reduce(lambda q, x: q | Q(project=x), user_projects, Q())
        filters = (filters) & Q(approved_role=False)
        return ProjectRole.objects.filter(filters)


class ProjectContributionApproveDeny(RedirectView):
    """
    View that will handle approval / denial of project contribution.
    Only the project owner can do so.

    Views inheriting this one can make use of self.projectrole to handle
     further operations.
    """
    # TODO project owner required
    pattern_name = 'projects:approve-contributions-list'

    def __init__(self):
        self.projectrole = ProjectRole.objects.none()

    def get_redirect_url(self, **kwargs):
        project = get_object_or_404(Project, pk=kwargs['pk'])
        user = get_object_or_404(User, pk=kwargs['user'])
        self.projectrole = get_object_or_404(ProjectRole,
                                             project=project, user=user)
        return reverse(self.pattern_name)


class ProjectContributionApproveView(ProjectContributionApproveDeny):
    """
    View that will handle the approval of project, given that the project exists
     and the user is its owner.
    Approved attribute will be set to true.
    """
    def get_redirect_url(self, **kwargs):
        redirect = super(ProjectContributionApproveView, self)\
            .get_redirect_url(**kwargs)
        self.projectrole.approved_role = True
        self.projectrole.save()
        return redirect


class ProjectContributionDenyView(ProjectContributionApproveDeny):
    """
    View that will handle the denial of project, given that the project exists
     and the user is its owner.
    Petition will be removed.
    """
    def get_redirect_url(self, **kwargs):
        redirect = super(ProjectContributionDenyView, self)\
            .get_redirect_url(**kwargs)
        self.projectrole.delete()
        return redirect
