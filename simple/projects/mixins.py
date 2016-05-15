from django.shortcuts import get_object_or_404
from core.mixins import OwnerRequiredMixin, ScientistRequiredMixin
from projects.models import Project
from django.views.generic import UpdateView


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


class ProjectEditMixin(OwnerRequiredMixin,ScientistRequiredMixin, UpdateView):
    model = Project

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.project = Project.objects.get(id=self.kwargs['pk'])
        return super(ProjectEditMixin, self).form_valid(form)
