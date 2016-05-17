from django.conf.urls import url

from projects.comments.views import CommentAdd, CommentEdit, CommentDelete

urlpatterns = [
    # Create new comment
    url(
        r'^\/new',
        CommentAdd.as_view(),
        name='comment_add'
    ),

    # Edit a specific comment
    url(
        r'^\/(?P<pk>\d+)/edit$',
        CommentEdit.as_view(),
        name='comment_edit'
    ),

    # Delete a specific comment
    url(
        r'^\/(?P<pk>\d+)/delete$',
        CommentDelete.as_view(),
        name='comment_delete'
    ),
]
