from django.conf.urls import url

from .views import ProjectDetail, ProjectList, ProjectNewView,\
    ProjectApproveList

urlpatterns = [
    # List of Projects
    url(
        r'^$',
        ProjectList.as_view(),
        name='list'
    ),

    # Project details
    url(
        r'^\/(?P<pk>\d+)$',
        ProjectDetail.as_view(),
        name='detail'
    ),

    # New project
    url(
        r'^\/new$',
        ProjectNewView.as_view(),
        name='new'
    ),

    # Approve / deny projects
    url(
        r'^\/approve$',
        ProjectApproveList.as_view(),
        name='approve-projects'
    ),
]
