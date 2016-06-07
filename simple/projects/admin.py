from django.contrib import admin

from projects.abstract_models import ProjectAttachment
from projects.forms import ProjectRoleNewAdminForm, ProjectRoleEditAdminForm
from .models import Project, ProjectRole, ProjectTechnicalRequest, ProjectLog, \
    ProjectRating, ProjectFavorite


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created')


class ProjectAttachmentAdmin(admin.ModelAdmin):
    list_display = ('project', 'object')


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

admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectAttachment, ProjectAttachmentAdmin)
admin.site.register(ProjectRole, ProjectRoleAdmin)
admin.site.register(ProjectRating, ProjectRatingAdmin)
admin.site.register(ProjectFavorite, ProjectFavoriteAdmin)
admin.site.register(ProjectLog, ProjectLogAdmin)
admin.site.register(ProjectTechnicalRequest, ProjectTechnicalRequestAdmin)
