from django.conf.urls import url

from users.views import RegisterView, LoginView, AccountView, UserList, SearchUser

urlpatterns = [
    url(r'^\/login$', LoginView.as_view(), name='login'),
    url(r'^\/signup$', RegisterView.as_view(), name='signup'),
    url(r'^\/(?P<pk>\d+)$', AccountView.as_view(), name='account'),
    url(r'^$', UserList.as_view(), name='user-list'),
    # Search User
    url(
        r'^\/search/(?P<firstname>.*)/$',
        SearchUser.as_view(),
        name='search-user'
    )
]
