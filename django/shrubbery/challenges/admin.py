from django.contrib import admin

from .models import Challenge, ChallengeComment


class ChallengeAdmin(admin.ModelAdmin):
    model = Challenge
    ordering = ('creation_date', 'title', 'author')
    search_fields = ('creation_date', 'title', 'title', 'author')
    list_display = ('title', 'creation_date', 'deadline', 'author')
    list_filter = ('hidden', 'verified')
    fieldsets = (
            (None, {
                "fields": (
                   ('title', 'content', 'creation_date', 'author',
                    'deadline', 'points', 'sanity_test', 'full_test',
                    'hidden', 'verified', 'executing_tests')
                ),
            }),
        )
    add_fieldsets = (
        (None, {
            'fields': ('title', 'content', 'creation_date', 'author',
                       'deadline', 'points', 'sanity_test', 'full_test',
                       'hidden', 'verified', 'executing_tests')
        }),
    )


class ChallengeCommentAdmin(admin.ModelAdmin):
    model = ChallengeComment
    ordering = ('date', 'author')
    search_fields = ('date', 'author', 'challenge', 'content')
    list_display = ('date', 'author', 'challenge')
    list_filter = ('author', 'challenge')
    fieldsets = (
            (None, {
                "fields": (
                   ('date', 'author', 'challenge', 'content', 'starred')
                ),
            }),
        )
    add_fieldsets = (
        (None, {
            'fields': ('date', 'author', 'challenge', 'content', 'starred')
        }),
    )

admin.site.register(Challenge, ChallengeAdmin)
admin.site.register(ChallengeComment, ChallengeCommentAdmin)
