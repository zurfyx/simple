from django.views.generic import CreateView, UpdateView, DeleteView


from projects.models import Project
from .models import Comment
from core.mixins import CustomLoginRequiredMixin, OwnerRequiredMixin


class CommentAddMixin(CustomLoginRequiredMixin, CreateView):
    model = Comment

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.project = Project.objects.get(id=self.kwargs['project'])
        return super(CommentAddMixin, self).form_valid(form)


class CommentEditMixin(OwnerRequiredMixin, UpdateView):
    model = Comment

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.project = Project.objects.get(id=self.kwargs['project'])
        return super(CommentEditMixin, self).form_valid(form)


class CommentDeleteMixin(DeleteView):
    pass
