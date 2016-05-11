from django.contrib import admin

from .models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ('content_shortener', 'project', 'user',)

    def content_shortener(self, instance):
        content = instance.content
        return content if len(content) < 30 else content[:30] + '...'

    content_shortener.short_description = 'Content'

admin.site.register(Comment, CommentAdmin)
