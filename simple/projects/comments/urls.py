from django.conf.urls import url

from .views import CommentAdd, CommentEdit

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
]
