from annoying.functions import get_object_or_None
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db import transaction
from django.db.models import Q
from django.http.response import JsonResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.utils.functional import SimpleLazyObject
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView
from django.views.generic.base import RedirectView, TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from core.mixins import CustomLoginRequiredMixin, HeadOfDepartmentMixin
from django.core.mail import EmailMessage
from core.utils import WordFilter
from projects import constants
from projects.abstract_models import ProjectAttachment
from projects.forms import ProjectNewForm, ProjectEditForm, ProjectContributeForm, ProjectQuestionForm, ProjectAnswerForm
from projects.mixins import ApprovedProjectRequiredMixin, ProjectAddQuestionMixin
from users.models import User
from mixins import ProjectEditMixin
from .models import Project, ProjectRole, ProjectRating, ProjectTechnicalRequest, ProjectFavorite


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
        return self.model.objects.filter(user=self.kwargs['user'])

    def get_context_data(self, **kwargs):
        context = super(UserProjectList, self).get_context_data(**kwargs)
        if type(self.kwargs['user']) != SimpleLazyObject:
            context['user'] = get_object_or_404(User, id=self.kwargs['user'])
        return context


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

    def get_object(self, queryset=None):
        obj = get_object_or_404(self.model, pk=self.kwargs['pk'])
        obj.increase_visits()
        obj.save()
        return obj

    def get_context_data(self, **kwargs):
        context = super(ProjectDetail, self).get_context_data(**kwargs)
        context['user_project_rating'] = \
            get_object_or_None(ProjectRating,
                               project=self.kwargs['pk'],
                               user=self.request.user) \
            if self.request.user.is_authenticated() else None
        context['user_project_role'] = \
            get_object_or_None(ProjectRole,
                               project=self.kwargs['pk'],
                               user=self.request.user)

        return context


class SearchProject(ListView):
    """
    Display project search.
    If an user input a project's title, it shows the project. Else if, it shows No Results
    """
    model = Project
    context_object_name = 'projects'
    template_name = 'projects/list.html'

    def get_queryset(self):
        filter = self.kwargs['title']
        search = self.model.objects.filter(title__icontains=filter)
        return search


class ProjectNewView(CustomLoginRequiredMixin, CreateView):
    template_name = 'projects/new.html'
    form_class = ProjectNewForm
    success_url = 'projects:pending-approval'

    def _create_owner_role(self, project, user):
        """
        Owner is always a scientist of the project
        """
        project_role = ProjectRole(project=project, user=user,
                                   role=constants.ProjectRoles.SCIENTIST,
                                   approved_role=True)
        project_role.save()

    def form_valid(self, form):
        project = form.save(commit=False)
        project.user = self.request.user
        form.instance.title = WordFilter().clean(form.instance.title)
        form.instance.body = WordFilter().clean(form.instance.body)
        project.save()

        # save attachments
        for each in form.cleaned_data['attachments']:
            ProjectAttachment.objects.create(project=project, object=each)

        # create owner role
        self._create_owner_role(project, project.user)

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
    success_url = 'projects:contribute'

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
    Displays a list of user projects, that have users who are pending a
    contribution approval.
    """
    # TODO project owner required
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
    # TODO POST request
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


class ProjectEdit(ProjectEditMixin):
    # TODO not edit user
    template_name = 'projects/edit.html'
    context_object_name = 'project'
    form_class = ProjectEditForm

    def form_valid(self, form):
        # word filters
        form.instance.body = WordFilter().clean(form.instance.body)

        # save attachments
        for each in form.cleaned_data['attachments']:
            ProjectAttachment.objects.create(project=form.instance, object=each)

        return super(ProjectEdit, self).form_valid(form)

    def get_success_url(self):
        project = Project.objects.get(pk=self.kwargs['pk'])
        user = self.request.user
        email = EmailMessage('Simple Technical Request', 'Your project '+str(project.title)+' has been edited by '+ str(user.first_name) , to =[project.user])
        email.send()
        return reverse('projects:detail', args=[self.kwargs['pk']])


class ProjectTechnicalRequestList(ListView):
    model = ProjectTechnicalRequest
    context_object_name = 'questions'
    template_name = 'projects/technical-requests.html'
    ordering = ['-created']

    def get_queryset(self):
        return self.model.objects.filter(project=self.kwargs['project'])

    def get_context_data(self, **kwargs):
        context = super(ProjectTechnicalRequestList, self).get_context_data(**kwargs)
        context['project'] = get_object_or_404(Project, id=self.kwargs['project'])
        return context


class ProjectTechnicalRequestNewView(ProjectAddQuestionMixin):
    template_name = 'projects/technical-request-new.html'
    form_class = ProjectQuestionForm

    def form_valid(self, form):
        form.instance.question = WordFilter().clean(form.instance.question)
        return super(ProjectTechnicalRequestNewView, self).form_valid(form)

    def get_success_url(self):
        return reverse('projects:technical-requests', args=[self.kwargs['project']])

    def get_context_data(self, **kwargs):
        context = super(ProjectTechnicalRequestNewView, self)\
            .get_context_data(**kwargs)
        context['project'] = get_object_or_404(Project, id=self.kwargs['project'])
        return context


class ProjectTechnicalRequestAnswerDetail(DetailView):
    model = ProjectTechnicalRequest
    template_name = 'projects/technical-request-answer.html'
    context_object_name = 'question'

    def get_context_data(self, **kwargs):
        context = super(ProjectTechnicalRequestAnswerDetail, self)\
            .get_context_data(**kwargs)
        return context


class ProjectTechnicalRequestAnswerNewView(UpdateView):
    model = ProjectTechnicalRequest
    template_name = 'projects/technical-request-answer-new.html'
    context_object_name = 'question'
    form_class = ProjectAnswerForm

    def form_valid(self, form):
        form.instance.answer = WordFilter().clean(form.instance.answer)
        return super(ProjectTechnicalRequestAnswerNewView, self).form_valid(form)

    def get_success_url(self):
        question = ProjectTechnicalRequest.objects.get(pk=self.kwargs['pk'])
        question.replied = True
        question.save()
        return reverse('projects:technical-request-answer',
                       args=[self.kwargs['project'], self.kwargs['pk']])


class VoteView(CustomLoginRequiredMixin, ApprovedProjectRequiredMixin,
               RedirectView):
    """
    Handles a project vote (either up or down).
    """
    pattern_name = 'projects:detail'

    def get_vote(self):
        self.project = get_object_or_404(Project, id=self.kwargs['pk'])
        self.user = self.request.user

        current_project_rating = get_object_or_None(ProjectRating,
                                                    project=self.project,
                                                    user=self.user)

        return current_project_rating if current_project_rating is not None \
            else ProjectRating(project=self.project, user=self.user)

    def post(self, request, *args, **kwargs):
        project = get_object_or_404(Project, id=self.kwargs['pk'])
        return JsonResponse({'upvotes': project.upvotes,
                             'downvotes': project.downvotes})

    def get_redirect_url(self, *args, **kwargs):
        return reverse(self.pattern_name, args=[self.kwargs['pk']])


class UpvoteView(VoteView):

    @method_decorator(csrf_protect)
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        project_rating = self.get_vote()
        if project_rating.rating is None:
            # new vote => +1 total upvotes
            self.project.upvotes += 1
            self.project.save()
        elif project_rating.is_downvoted():
            # old vote => -1 total downvotes +1 total upvotes
            self.project.downvotes -= 1
            self.project.upvotes += 1
            self.project.save()

        project_rating.upvote()
        project_rating.save()

        return super(UpvoteView, self).post(request, *args, **kwargs)


class DownvoteView(VoteView):

    @method_decorator(csrf_protect)
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        project_rating = self.get_vote()
        if project_rating.rating is None:
            # new vote => +1 total downvotes
            self.project.downvotes += 1
            self.project.save()
        elif project_rating.is_upvoted():
            # old vote => -1 total upvotes +1 total downvotes
            self.project.upvotes -= 1
            self.project.downvotes += 1
            self.project.save()

        project_rating.downvote()
        project_rating.save()

        return super(DownvoteView, self).post(request, *args, **kwargs)


class FavoritesView(ListView):
    template_name = 'projects/favorites.html'
    model = ProjectFavorite
    context_object_name = 'favorites'

    def queryset(self):
        return self.model.objects.filter(user=self.request.user)


def favorite_create(request):
    if request.method == 'POST':
        project_id = request.POST.get('project')
        project = Project.objects.get(pk=project_id)
        user = request.user
        try:
            ProjectFavorite.objects.get(project=project, user=user)
            return render(request, 'projects/favorites.html', {'exist': '1', 'project': project.title})

        except:
            favorite = ProjectFavorite(project=project, user=user)
            favorite.save()
            return render(request, 'projects/favorites.html', {'added': '1', 'project': project.title})


def favorite_delete(request):
    project_id = request.POST.get('project')
    project = Project.objects.get(pk=project_id)
    favorite = ProjectFavorite.objects.get(project=project, user=request.user)
    favorite.delete()
    return HttpResponseRedirect('/projects/favorites')


class NotificationsView(ListView):
    template_name = 'projects/notifications.html'
    model = ProjectTechnicalRequest
    context_object_name = 'questions'

    def queryset(self):
        return self.model.objects.filter(to_user=self.request.user, replied=False)


def revokeproject(request):
    project_id = request.POST.get('project')
    project = Project.objects.get(pk=project_id)
    projectrole = ProjectRole.objects.get(project=project, user= request.user)
    projectrole.delete()
    return HttpResponseRedirect('/projects/'+ project_id)
