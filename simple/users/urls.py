from django.conf.urls import url

from users.views import RegisterView, LoginView

urlpatterns = [
    url(r'^\/login', LoginView.as_view(), name='login'),
    url(r'^\/signup', RegisterView.as_view(), name='register'),
]
