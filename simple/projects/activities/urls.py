from django.conf.urls import url

from .views import ActivityList, ActivityNewView, ActivityDetailView, \
    ActivityResponseNewView

urlpatterns = [
    # List of activities
    url(
        r'^$',
        ActivityList.as_view(),
        name='list'
    ),

    # Add new activity
    url(
        r'^\/new$',
        ActivityNewView.as_view(),
        name='new'
    ),

    # Activity details
    url(
        r'^\/(?P<pk>\d+)$',
        ActivityDetailView.as_view(),
        name='detail'
    ),

    # Edit activity

    # Add new response
    url(
        r'^\/(?P<activity>\d+)/response/new$',
        ActivityResponseNewView.as_view(),
        name='response-new'
    ),

    # Edit response
]
