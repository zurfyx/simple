from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import View

from projects.models import Project
from .models import ProjectActivity


class ActivityBaseMixin(View):
    def get_context_data(self, **kwargs):
        context = super(ActivityBaseMixin, self).get_context_data(**kwargs)
        context['project'] = get_object_or_404(Project, id=self.kwargs['project'])
        return context


class ActivityOpenMixin(object):
    """
    Checks if the activity is open by its starting & ending date, and the
    current server date.
    If the activity is not open, it will redirect to the activity page.
    Expects 1. <activity> or 2. <pk> => activity
    """
    def get_activity(self):
        activity_id = self.kwargs['activity'] if 'activity' in self.kwargs \
            else self.kwargs['pk']
        activity = get_object_or_404(ProjectActivity, id=activity_id)
        return activity

    def dispatch(self, request, *args, **kwargs):
        activity = self.get_activity()
        if activity.is_closed():
            args = [activity.project.id, activity.id]
            return redirect(reverse('projects:activities:detail', args=args))
        return super(ActivityOpenMixin, self).dispatch(request, *args, **kwargs)
