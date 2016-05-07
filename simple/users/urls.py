from django.conf.urls import url
from django.views.generic import UpdateView
from models import User
from forms import UserCreationForm

from users.views import RegisterView, LoginView, AccountView

urlpatterns = [
    url(r'^\/login$', LoginView.as_view(), name='login'),
    url(r'^\/signup$', RegisterView.as_view(), name='signup'),
    url(r'^\/(?P<pk>\d+)$', AccountView.as_view(), name='account'),
    url(r'^\/(?P<pk>\d+)/edit-user$',
        UpdateView.as_view(
            model = User,
            template_name = 'users/form.html',
            form_class = UserCreationForm,
            success_url = 'users:left-sidebar'

        ),
        name='edit-user'
    ),

]
