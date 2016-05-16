from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^users', include('users.urls', namespace='users')),
    url(r'^projects', include('projects.urls', namespace='projects')),
    url(r'^', include('home.urls', namespace='home')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
