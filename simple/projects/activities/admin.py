from django.contrib import admin

from .models import ProjectActivity, ProjectActivityResponse, \
    ProjectActivityResponseAttachment, ProjectActivityAttachment


class ProjectActivityAdmin(admin.ModelAdmin):
    list_display = ('project', 'user', 'title', 'start_date', 'due_date')


class ProjectActivityAttachmentAdmin(admin.ModelAdmin):
    list_display = ('activity', 'object')


class ProjectActivityResponseAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity')


class ProjectActivityResponseAttachmentAdmin(admin.ModelAdmin):
    list_display = ('response', 'object')

admin.site.register(ProjectActivity, ProjectActivityAdmin)
admin.site.register(ProjectActivityAttachment, ProjectActivityAttachmentAdmin)
admin.site.register(ProjectActivityResponse, ProjectActivityResponseAdmin)
admin.site.register(ProjectActivityResponseAttachment, ProjectActivityResponseAttachmentAdmin)
