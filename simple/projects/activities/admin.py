from django.contrib import admin

from .models import ProjectActivity, ProjectActivityResponse


class ProjectActivityAdmin(admin.ModelAdmin):
    list_display = ('project', 'user', 'title', 'start_date', 'due_date')


class ProjectActivityResponseAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity')

admin.site.register(ProjectActivity, ProjectActivityAdmin)
admin.site.register(ProjectActivityResponse, ProjectActivityResponseAdmin)
