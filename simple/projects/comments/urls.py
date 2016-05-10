from django.conf.urls import url

from .views import CommentAdd

urlpatterns = [
    # Create new comment
    url(
        r'^\/new',
        CommentAdd.as_view(),
        name='comment_add'
    ),
]
