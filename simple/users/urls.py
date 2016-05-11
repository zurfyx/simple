from django.conf.urls import url
from django.views.generic import UpdateView
from models import User
from forms import UserCreationForm
from users.views import RegisterView, LoginView, AccountView, UserList, SearchUser

urlpatterns = [
    url(r'^\/login$', LoginView.as_view(), name='login'),
    url(r'^\/signup$', RegisterView.as_view(), name='signup'),
    url(r'^\/(?P<pk>\d+)$', AccountView.as_view(), name='account'),
    url(r'\/$', UserList.as_view(), name='list'),
    url(r'^\/(?P<pk>\d+)/edit-user$',
        UpdateView.as_view(
            model = User,
            template_name = 'users/forms.html',
            form_class = UserCreationForm,
            success_url = 'users:left-sidebar'
        ),
        name='edit-user'
        ),
    # Search User
    url(
        r'^\/search/(?P<first_name>.*)/$',
        SearchUser.as_view(),
        name='search-user'
    )
]
