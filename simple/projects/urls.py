from django.conf.urls import url, include
from views import ProjectEdit
from forms import ProjectQuestionForm
from .views import ProjectDetail, ProjectList, ProjectNewView,\
    ProjectApproveList, ProjectApproveView, ProjectDenyView, \
    ProjectContributeView, ProjectPendingApproval, \
    ProjectApproveContributionList, UserProjectList, \
    ProjectContributionApproveView, ProjectContributionDenyView,\
    SearchProject, UpvoteView, DownvoteView, ProjectQuestions, \
    ProjectQuestionAdd, FavoritesView,ProjectAnswer, ProjectAddAnswer

urlpatterns = [
    # Include comments application
    url(
        r'^\/(?P<project>\d+)/comments',
        include('projects.comments.urls', namespace='comments')
    ),

    # Include activities application
    url(
       r'^\/(?P<project>\d+)/activities',
       include('projects.activities.urls', namespace='activities')
    ),

    # List of Projects
    url(
        r'^$',
        ProjectList.as_view(),
        name='list'
    ),

    # List of Projects by User
    url(
        r'^\/user/(?P<user>\d+)$',
        UserProjectList.as_view(),
        name='user-list'
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

    # Search Project
    url(
        r'^\/search/(?P<title>.*)/$',
        SearchProject.as_view(),
        name='search-project'
    ),

    # Pending approval message view shown after project creation
    url(
        r'^\/pending-approval',
        ProjectPendingApproval.as_view(),
        name='pending-approval'
    ),

    # Approve / deny projects list
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

    # Approve / deny contribution list
    url(
        r'\/approve-contributions$',
        ProjectApproveContributionList.as_view(),
        name='approve-contributions-list'
    ),

    # Approve contribution
    url(
        r'\/approve-contribution/project/(?P<pk>\d+)/user/(?P<user>\d+)/$',
        ProjectContributionApproveView.as_view(),
        name='approve-contribution'
    ),

    # Deny contribution
    url(
        r'\/deny-contribution/project/(?P<pk>\d+)/user/(?P<user>\d+)$',
        ProjectContributionDenyView.as_view(),
        name='deny-contribution'
    ),

    # Edit Project
    url(
        r'^\/(?P<pk>\d+)/edit$',
        ProjectEdit.as_view(),
        name='edit'
    ),

    # Question list
    url(
        r'^\/(?P<project>\d+)/questions/$',
        ProjectQuestions.as_view(),
        name='question'
    ),

    # Add question
    url(
        r'^\/(?P<project>\d+)/questions/add/$',
        ProjectQuestionAdd.as_view(template_name = 'projects/question_add.html',form_class = ProjectQuestionForm),
        name='question_add'
    ),

    # See answer
    url(
        r'^\/(?P<project>\d+)/questions/(?P<pk>\d+)$',
        ProjectAnswer.as_view(),
        name='answer'
    ),

    # Add answer
    url(
        r'^\/(?P<project>\d+)/questions/(?P<pk>\d+)/addanswer$',
        ProjectAddAnswer.as_view(),
        name='answer_add'
    ),


    # Vote up project
    url(
        r'^\/(?P<pk>\d+)/vote/up$',
        UpvoteView.as_view(),
        name='upvote'
    ),

    # Vote down project
    url(
        r'^\/(?P<pk>\d+)/vote/down$',
        DownvoteView.as_view(),
        name='downvote'
    ),

    # Favorites projects
    url(
        r'^\/favorites$',
        FavoritesView.as_view(),
        name='favorites'
    ),

]
