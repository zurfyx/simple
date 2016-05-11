from django.contrib import admin

from .models import Project, ProjectRole, ProjectActivityResponse, \
    ProjectActivity, ProjectTechnicalRequest, ProjectLog, ProjectRating


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'created')


class ProjectRoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'role')


class ProjectRatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'rating')


class ProjectLogAdmin(admin.ModelAdmin):
    list_display = ('project', 'type')


class ProjectTechnicalRequestAdmin(admin.ModelAdmin):
    list_display = ('project', 'question')


class ProjectActivityAdmin(admin.ModelAdmin):
    list_display = ('project', 'owner', 'title', 'start_date', 'due_date')


class ProjectActivityResponseAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity')

admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectRole, ProjectRoleAdmin)
admin.site.register(ProjectRating, ProjectRatingAdmin)
admin.site.register(ProjectLog, ProjectLogAdmin)
admin.site.register(ProjectTechnicalRequest, ProjectTechnicalRequestAdmin)
admin.site.register(ProjectActivity, ProjectActivityAdmin)
admin.site.register(ProjectActivityResponse, ProjectActivityResponseAdmin)
