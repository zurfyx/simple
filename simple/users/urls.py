from django.conf.urls import url

from users.views import RegisterView, LoginView, AccountView

urlpatterns = [
    url(r'^\/login$', LoginView.as_view(), name='login'),
    url(r'^\/signup$', RegisterView.as_view(), name='signup'),
    url(r'^\/(?P<pk>\d+)$', AccountView.as_view(), name='account'),
]
