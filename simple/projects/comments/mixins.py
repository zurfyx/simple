from django.views.generic import CreateView, UpdateView, DeleteView

from core.mixins import CustomLoginRequiredMixin, OwnerRequiredOrModeratorMixin
from projects.comments.models import Comment
from projects.models import Project


class CommentAddMixin(CustomLoginRequiredMixin, CreateView):
    model = Comment

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.project = Project.objects.get(id=self.kwargs['project'])
        return super(CommentAddMixin, self).form_valid(form)


class CommentEditMixin(OwnerRequiredOrModeratorMixin, UpdateView):
    model = Comment

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.project = Project.objects.get(id=self.kwargs['project'])
        return super(CommentEditMixin, self).form_valid(form)


class CommentDeleteMixin(OwnerRequiredOrModeratorMixin, DeleteView):
    model = Comment

