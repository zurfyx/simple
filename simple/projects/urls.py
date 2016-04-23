from django.conf.urls import url

from .views import ProjectDetail, ProjectList

urlpatterns = [
    # List of Projects
    url(
        r'^$',
        ProjectList.as_view(),
        name='project_list'
    ),

    # Project details
    url(
        r'^\/(?P<pk>\d+)$',
        ProjectDetail.as_view(),
        name='project_detail'
    )
]