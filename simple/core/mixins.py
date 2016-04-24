from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404


class CustomLoginRequiredMixin(LoginRequiredMixin):
    login_url = 'users:login'
    redirect_field_name = 'next'


class HeadOfDepartmentMixin(CustomLoginRequiredMixin):
    """
    Either a Head of Department or Administrator is required to be logged in.
    Otherwise, it will return a 404 response.
    """

    def dispatch(self, request, **kwargs):
        user = request.user
        if user.is_authenticated() \
                and user.role != 3 and user.is_staff is False:
            raise Http404('Not a Head of Department')
        return super(HeadOfDepartmentMixin, self).dispatch(request, **kwargs)
