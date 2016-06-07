from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView

from core.mixins import OwnerRequiredMixin
from core.utils import WordFilter
from projects.models import Project
from .models import Comment, CommentAttachment
from .forms import CommentAddForm, CommentEditForm
from .mixins import CommentEditMixin, CommentDeleteMixin, CommentBaseMixin


class CommentAdd(OwnerRequiredMixin, CommentBaseMixin, CreateView):
    template_name = 'projects/comments/comment_add.html'
    model = Comment
    form_class = CommentAddForm

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.user = self.request.user
        comment.project = get_object_or_404(Project, id=self.kwargs['project'])
        comment.content = WordFilter().clean(form.instance.content)
        comment.save()

        # save attachments
        for each in form.cleaned_data['attachments']:
            CommentAttachment.objects.create(comment=comment,
                                             object=each)

        self.object = comment
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('projects:detail', args=[self.kwargs['project']]) + \
               '#comment_' + str(self.object.id)


class CommentEdit(CommentEditMixin):
    template_name = 'projects/comments/comment_edit.html'
    form_class = CommentEditForm

    def form_valid(self, form):
        # word filters
        form.instance.content = WordFilter().clean(form.instance.content)

        # save attachments
        for each in form.cleaned_data['attachments']:
            CommentAttachment.objects.create(comment=form.instance, object=each)

        return super(CommentEdit, self).form_valid(form)

    def get_success_url(self):
        return reverse('projects:detail', args=[self.kwargs['project']]) + \
               '#comment_' + str(self.object.id)


class CommentDelete(CommentDeleteMixin):
    template_name = 'projects/comments/comment_delete.html'

    def get_success_url(self):
        return reverse('projects:detail', args=[self.kwargs['project']]) + \
               '#comment_' + str(self.object.id)
