from django.contrib import admin

from .models import (ChallengeSolution, ChallengeSolutionHistory,
                     ChallengeSolutionComment, ChallengeSolutionInlineComment,
                     ChallengeSolutionHistoryInlineComment,
                     ChallengeSolutionTeacherPoints)


class ChallengeSolutionAdmin(admin.ModelAdmin):
    model = ChallengeSolution
    ordering = ('challenge', 'author')
    search_fields = ('challenge', 'author')
    list_display = ('challenge', 'author', 'upload_date')
    list_filter = ('challenge', 'author')
    fieldsets = (
            (None, {
                "fields": (
                   ('challenge', 'author', 'content', 'upload_date', 'points',
                       'line_count', 'result', 'passed_tests', 'failed_tests',
                       'subscribers', 'commit_message')
                ),
            }),
        )
    add_fieldsets = (
        (None, {
            'fields': ('challenge', 'author', 'content', 'upload_date', 'points',
                       'line_count', 'result', 'passed_tests', 'failed_tests',
                       'subscribers', 'commit_message')
        }),
    )


class ChallengeSolutionHistoryAdmin(admin.ModelAdmin):
    model = ChallengeSolutionHistory
    ordering = ('challenge', 'author')
    search_fields = ('challenge', 'author')
    list_display = ('challenge', 'author', 'upload_date')
    list_filter = ('challenge', 'author')
    fieldsets = (
            (None, {
                "fields": (
                   ('challenge', 'author', 'solution', 'content', 'upload_date', 'diff', 'commit_message')
                ),
            }),
        )
    add_fieldsets = (
        (None, {
            'fields': ('challenge', 'author', 'solution', 'content', 'upload_date', 'diff', 'commit_message')
        }),
    )

class ChallengeSolutionCommentAdmin(admin.ModelAdmin):
    model = ChallengeSolutionComment
    ordering = ('date', 'author')
    search_fields = ('date', 'author', 'solution', 'content')
    list_display = ('date', 'author', 'solution')
    list_filter = ('author', 'solution')
    fieldsets = (
            (None, {
                "fields": (
                   ('date', 'author', 'solution', 'content', 'starred')
                ),
            }),
        )
    add_fieldsets = (
        (None, {
            'fields': ('date', 'author', 'solution', 'content', 'starred')
        }),
    )


class ChallengeSolutionInlineCommentAdmin(admin.ModelAdmin):
    model = ChallengeSolutionInlineComment
    ordering = ('date', 'author')
    search_fields = ('date', 'author', 'solution', 'content')
    list_display = ('date', 'author', 'solution', 'line')
    list_filter = ('author', 'solution')
    fieldsets = (
            (None, {
                "fields": (
                   ('date', 'author', 'solution', 'content', 'line')
                ),
            }),
        )
    add_fieldsets = (
        (None, {
            'fields': ('date', 'author', 'solution', 'content', 'line')
        }),
    )


class ChallengeSolutionHistoryInlineCommentAdmin(admin.ModelAdmin):
    model = ChallengeSolutionHistoryInlineComment
    ordering = ('date', 'author')
    search_fields = ('date', 'author', 'solution', 'content')
    list_display = ('date', 'author', 'solution', 'line')
    list_filter = ('author', 'solution')
    fieldsets = (
            (None, {
                "fields": (
                   ('date', 'author', 'solution', 'history', 'content', 'line')
                ),
            }),
        )
    add_fieldsets = (
        (None, {
            'fields': ('date', 'author', 'solution', 'history', 'content', 'line')
        }),
    )


class ChallengeSolutionTeacherPointsAdmin(admin.ModelAdmin):
    model = ChallengeSolutionTeacherPoints
    ordering = ('solution', 'points')
    search_fields = ('solution',)
    list_display = ('solution', 'points')
    list_filter = ('solution', )
    fieldsets = (
            (None, {
                "fields": (
                   ('solution', 'points')
                ),
            }),
        )
    add_fieldsets = (
        (None, {
            'fields': ('solution', 'points')
        }),
    )



admin.site.register(ChallengeSolution, ChallengeSolutionAdmin)
admin.site.register(ChallengeSolutionHistory, ChallengeSolutionHistoryAdmin)
admin.site.register(ChallengeSolutionComment, ChallengeSolutionCommentAdmin)
admin.site.register(ChallengeSolutionInlineComment, ChallengeSolutionInlineCommentAdmin)
admin.site.register(ChallengeSolutionHistoryInlineComment, ChallengeSolutionHistoryInlineCommentAdmin)
admin.site.register(ChallengeSolutionTeacherPoints, ChallengeSolutionTeacherPointsAdmin)
