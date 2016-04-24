from django.contrib import admin

from .models import Project, ProjectRole


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'created')


class ProjectRoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'role')

admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectRole, ProjectRoleAdmin)
