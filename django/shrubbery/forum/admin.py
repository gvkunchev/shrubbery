from django.contrib import admin
from .models import Forum, ForumComment


class ForumAdmin(admin.ModelAdmin):
    model = Forum
    ordering = ('date', 'author')
    search_fields = ('date', 'author', 'title', 'content')
    list_display = ('title', 'date', 'author')
    list_filter = ('author',)
    fieldsets = (
            (None, {
                "fields": (
                   ('date', 'author', 'title', 'content')
                ),
            }),
        )
    add_fieldsets = (
        (None, {
            'fields': ('date', 'author', 'title', 'content')
        }),
    )


class ForumCommentAdmin(admin.ModelAdmin):
    model = ForumComment
    ordering = ('date', 'author')
    search_fields = ('date', 'author', 'forum', 'parent', 'content')
    list_display = ('date', 'author', 'forum')
    list_filter = ('author', 'forum')
    fieldsets = (
            (None, {
                "fields": (
                   ('date', 'author', 'forum', 'parent', 'content', 'starred')
                ),
            }),
        )
    add_fieldsets = (
        (None, {
            'fields': ('date', 'author', 'forum', 'parent', 'content', 'starred')
        }),
    )

admin.site.register(Forum, ForumAdmin)
admin.site.register(ForumComment, ForumCommentAdmin)
