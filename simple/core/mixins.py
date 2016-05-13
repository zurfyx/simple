from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import Http404

from users import constants


class CustomLoginRequiredMixin(LoginRequiredMixin):
    login_url = 'users:login'
    redirect_field_name = 'next'


class BaseRoleRequiredMixin(object):
    def get_object(self, *args, **kwargs):
        super(BaseRoleRequiredMixin, self).get(*args, **kwargs)


class HeadOfDepartmentMixin(CustomLoginRequiredMixin):
    """
    Either a Head of Department or Administrator is required to be logged in.
    Otherwise, it will return a 404 response.
    """
    def dispatch(self, request, **kwargs):
        user = request.user
        if user.is_authenticated() \
                and user.role != constants.UserRoles.HEAD_OF_DEPARTMENT \
                and user.is_staff is False:
            raise Http404('Not a Head of Department')
        return super(HeadOfDepartmentMixin, self).dispatch(request, **kwargs)


class ModeratorRequiredMixin(CustomLoginRequiredMixin):
    """
    Either a Moderator or Administrator is required to be logged in.
    Otherwise, it will return a 404 response.
    """
    def dispatch(self, request, **kwargs):
        user = request.user
        if user.is_authenticated() \
                and user.role != constants.UserRoles.MODERATOR \
                and user.is_staff is False:
            raise Http404('Not a Moderator')
        return super(ModeratorRequiredMixin, self).dispatch(request, **kwargs)


class OwnerRequiredMixin(CustomLoginRequiredMixin):
    """
    The owner of the object is required to view THIS object.
    """

    def get_object(self, *args, **kwargs):
        obj = super(OwnerRequiredMixin, self).get_object(*args, **kwargs)
        if not obj.user == self.request.user:
            raise PermissionDenied('Not the owner')
        return obj


class OwnerRequiredOrModeratorMixin(OwnerRequiredMixin, ModeratorRequiredMixin):
    """
    Either Owner or Moderator are required to view THIS object.
    Thus, we are expecting that at least one of them does not throw
    PermissionDenied
    """

    def get_object(self, *args, **kwargs):
        try:
            return super(OwnerRequiredMixin, self).get_object(*args, **kwargs)
        except PermissionDenied:
            pass
        raise PermissionDenied('Not the Owner nor Moderator')


