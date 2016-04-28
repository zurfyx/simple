from django.conf.urls import url

from .views import ProjectDetail, ProjectList, ProjectNewView,\
    ProjectApproveList, ProjectApproveView, ProjectDenyView, \
    ProjectContributeView, ProjectPendingApproval

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

    # Pending approval message view shown after project creation
    url(
        r'^\/pending-approval',
        ProjectPendingApproval.as_view(),
        name='pending-approval'
    ),

    # Approve / deny projects
    url(
        r'^\/approve$',
        ProjectApproveList.as_view(),
        name='approve-list'
    ),

    # Approve project
    url(
        r'^\/approve/(?P<pk>\d+)$',
        ProjectApproveView.as_view(),
        name='approve-project'
    ),

    # Deny project
    url(
        r'^\/deny/(?P<pk>\d+)$',
        ProjectDenyView.as_view(),
        name='deny-project'
    ),

    # Contribute to project
    url(
        r'\/(?P<pk>\d+)/contribute$',
        ProjectContributeView.as_view(),
        name='contribute'
    ),
]
