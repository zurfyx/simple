from django.contrib import admin

from projects.comments.models import Comment, CommentAttachment


class CommentAdmin(admin.ModelAdmin):
    list_display = ('content_shortener', 'project', 'user',)

    def content_shortener(self, instance):
        content = instance.content
        return content if len(content) < 30 else content[:30] + '...'

    content_shortener.short_description = 'Content'


class CommentAttachmentAdmin(admin.ModelAdmin):
    list_display = ('comment', 'object')

admin.site.register(Comment, CommentAdmin)
admin.site.register(CommentAttachment, CommentAttachmentAdmin)
