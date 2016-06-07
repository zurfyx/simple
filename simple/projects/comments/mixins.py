from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic.base import View

from core.mixins import CustomLoginRequiredMixin, OwnerRequiredOrModeratorMixin, OwnerRequiredMixin
from projects.comments.models import Comment
from projects.models import Project


class CommentBaseMixin(View):
    def get_context_data(self, **kwargs):
        context = super(CommentBaseMixin, self).get_context_data(**kwargs)
        context['project'] = get_object_or_404(Project, id=self.kwargs['project'])
        return context


class CommentEditMixin(OwnerRequiredMixin, CommentBaseMixin, UpdateView):
    model = Comment

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.project = Project.objects.get(id=self.kwargs['project'])
        return super(CommentEditMixin, self).form_valid(form)


class CommentDeleteMixin(OwnerRequiredOrModeratorMixin, CommentBaseMixin, DeleteView):
    model = Comment

