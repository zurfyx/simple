from django.shortcuts import redirect


class NotLoginRequiredMixin(object):

    def dispatch(self, request, **kwargs):
        if request.user.is_authenticated():
            return redirect('/')
        return super(NotLoginRequiredMixin, self).dispatch(request, **kwargs)


