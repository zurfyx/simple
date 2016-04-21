from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    #url(r'^users', include('users.urls', namespace='users')),
    #url(r'^projects', include('projects.urls', namespace='projects')),
    #url(r'^$', include('home.urls', namespace='home'))
]
