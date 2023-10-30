from django.contrib import admin

from .models import (HomeworkSolution, HomeworkSolutionHistory,
                     HomeworkSolutionComment, HomeworkSolutionInlineComment,
                     HomeworkSolutionHistoryInlineComment,
                     HomeworkSolutionTeacherPoints)


class HomeworkSolutionAdmin(admin.ModelAdmin):
    model = HomeworkSolution
    ordering = ('homework', 'author')
    search_fields = ('homework', 'author')
    list_display = ('homework', 'author', 'upload_date')
    list_filter = ('homework', 'author')
    fieldsets = (
            (None, {
                "fields": (
                   ('homework', 'author', 'content', 'upload_date', 'points',
                       'line_count', 'result', 'passed_tests', 'failed_tests',
                       'subscribers', 'commit_message')
                ),
            }),
        )
    add_fieldsets = (
        (None, {
            'fields': ('homework', 'author', 'content', 'upload_date', 'points',
                       'line_count', 'result', 'passed_tests', 'failed_tests',
                       'subscribers', 'commit_message')
        }),
    )


class HomeworkSolutionHistoryAdmin(admin.ModelAdmin):
    model = HomeworkSolutionHistory
    ordering = ('homework', 'author')
    search_fields = ('homework', 'author')
    list_display = ('homework', 'author', 'upload_date')
    list_filter = ('homework', 'author')
    fieldsets = (
            (None, {
                "fields": (
                   ('homework', 'author', 'solution', 'content', 'upload_date', 'diff', 'commit_message')
                ),
            }),
        )
    add_fieldsets = (
        (None, {
            'fields': ('homework', 'author', 'solution', 'content', 'upload_date', 'diff', 'commit_message')
        }),
    )

class HomeworkSolutionCommentAdmin(admin.ModelAdmin):
    model = HomeworkSolutionComment
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


class HomeworkSolutionInlineCommentAdmin(admin.ModelAdmin):
    model = HomeworkSolutionInlineComment
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


class HomeworkSolutionHistoryInlineCommentAdmin(admin.ModelAdmin):
    model = HomeworkSolutionHistoryInlineComment
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


class HomeworkSolutionTeacherPointsAdmin(admin.ModelAdmin):
    model = HomeworkSolutionTeacherPoints
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



admin.site.register(HomeworkSolution, HomeworkSolutionAdmin)
admin.site.register(HomeworkSolutionHistory, HomeworkSolutionHistoryAdmin)
admin.site.register(HomeworkSolutionComment, HomeworkSolutionCommentAdmin)
admin.site.register(HomeworkSolutionInlineComment, HomeworkSolutionInlineCommentAdmin)
admin.site.register(HomeworkSolutionHistoryInlineComment, HomeworkSolutionHistoryInlineCommentAdmin)
admin.site.register(HomeworkSolutionTeacherPoints, HomeworkSolutionTeacherPointsAdmin)
