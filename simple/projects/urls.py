from django.conf.urls import url

from .views import ProjectDetailList, ProjectList

urlpatterns = [
    #List of Projects
    url(
        r'^$',
        ProjectList.as_view(),
        name='project_list'
    ),

    #Detail projects list
    url(
        r'^$',
        ProjectDetailList.as_view(),
        name='detail_project_list'
    )
]