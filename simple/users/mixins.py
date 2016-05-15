from django.shortcuts import redirect
from core.mixins import CustomLoginRequiredMixin
from models import User
from django.views.generic import UpdateView
class NotLoginRequiredMixin(object):

    def dispatch(self, request, **kwargs):
        if request.user.is_authenticated():
            return redirect('/')
        return super(NotLoginRequiredMixin, self).dispatch(request, **kwargs)


