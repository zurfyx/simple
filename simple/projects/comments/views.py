from django.core.urlresolvers import reverse

from .mixins import CommentAddMixin, CommentEditMixin, CommentDeleteMixin
from .forms import CommentAddForm, CommentEditForm


class CommentAdd(CommentAddMixin):
    template_name = 'projects/comments/comment_add.html'
    form_class = CommentAddForm

    def get_success_url(self):
        return reverse('projects:detail', args=[self.kwargs['project']]) + \
               '#comment_' + str(self.object.id)


class CommentEdit(CommentEditMixin):
    template_name = 'projects/comments/comment_edit.html'
    form_class = CommentEditForm

    def get_success_url(self):
        return reverse('projects:detail', args=[self.kwargs['project']]) + \
               '#comment_' + str(self.object.id)


class CommentDelete(CommentDeleteMixin):
    template_name = 'projects/comments/comment_delete.html'

    def get_success_url(self):
        return reverse('projects:detail', args=[self.kwargs['project']]) + \
               '#comment_' + str(self.object.id)
