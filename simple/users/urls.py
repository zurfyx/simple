from django.conf.urls import url
from models import User
from forms import UserCreationForm
from django.views.generic import UpdateView
from users.views import RegisterView, LoginView, AccountView, UserList, SearchUser

from users.views import RegisterView, LoginView, AccountView, UserList, \
    SearchUser, LogoutView

urlpatterns = [
    # login
    url(
        r'^\/login$',
        LoginView.as_view(),
        name='login'
    ),

    # logout
    url(
        r'^\/logout$',
        LogoutView.as_view(),
        name='logout'
    ),

    # sign up
    url(
        r'^\/signup$',
        RegisterView.as_view(),
        name='signup'
    ),

    # user account
    url(
        r'^\/(?P<pk>\d+)$',
        AccountView.as_view(),
        name='account'
    ),

    # user list
    url(
        r'^$',
        UserList.as_view(),
        name='list'
    ),

    # search user
    url(
        r'^\/search/(?P<first_name>.*)/$',
        SearchUser.as_view(),
        name='search-user'
    ),

    # edit user
    url(r'^\/(?P<pk>\d+)/edit$',
        UpdateView.as_view(
            model = User,
            template_name = 'users/form.html',
            form_class = UserCreationForm,

        ),
        name='edit-user'
    ),
]
