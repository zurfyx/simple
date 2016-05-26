from django.conf.urls import url

from .views import ActivityList, ActivityNewView

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

    # Edit activity

    # List of responses

    # Add new response

    # Edit response
]
