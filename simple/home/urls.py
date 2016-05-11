from django.conf.urls import url

from home.views import LandingView

urlpatterns = [
    # Landing page
    url('^$', LandingView.as_view(), name='landing'),
]
