from django.core.urlresolvers import reverse

from .mixins import CommentAddMixin
from .forms import CommendAddForm


class CommentAdd(CommentAddMixin):
    template_name = 'projects/comments/comment_add.html'
    form_class = CommendAddForm

    def get_success_url(self):
        return reverse('projects:detail', args=[self.kwargs['project']]) + \
               '#comment_' + str(self.object.id)
