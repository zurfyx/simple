from django.contrib import admin

from projects.forms import ProjectRoleNewAdminForm, ProjectRoleEditAdminForm
from .models import Project, ProjectRole, ProjectActivityResponse, \
    ProjectActivity, ProjectTechnicalRequest, ProjectLog, ProjectRating, \
    ProjectFavorite


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created')


class ProjectRoleAdmin(admin.ModelAdmin):
    form = ProjectRoleEditAdminForm
    add_form = ProjectRoleNewAdminForm
    list_display = ('user', 'project', 'role')


class ProjectRatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'rating')


class ProjectFavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'project')


class ProjectLogAdmin(admin.ModelAdmin):
    list_display = ('project', 'type')


class ProjectTechnicalRequestAdmin(admin.ModelAdmin):
    list_display = ('project', 'question')


class ProjectActivityAdmin(admin.ModelAdmin):
    list_display = ('project', 'user', 'title', 'start_date', 'due_date')


class ProjectActivityResponseAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity')

admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectRole, ProjectRoleAdmin)
admin.site.register(ProjectRating, ProjectRatingAdmin)
admin.site.register(ProjectFavorite, ProjectFavoriteAdmin)
admin.site.register(ProjectLog, ProjectLogAdmin)
admin.site.register(ProjectTechnicalRequest, ProjectTechnicalRequestAdmin)
admin.site.register(ProjectActivity, ProjectActivityAdmin)
admin.site.register(ProjectActivityResponse, ProjectActivityResponseAdmin)
