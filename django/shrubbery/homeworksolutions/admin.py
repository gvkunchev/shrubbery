from django.contrib import admin

from .models import HomeworkSolution, HomeworkSolutionHistory


class HomeworkSolutionAdmin(admin.ModelAdmin):
    model = HomeworkSolution
    ordering = ('homework', 'author')
    search_fields = ('homework', 'author')
    list_display = ('homework', 'author', 'upload_date')
    list_filter = ('homework', 'author')
    fieldsets = (
            (None, {
                "fields": (
                   ('homework', 'author', 'content', 'upload_date', 'points')
                ),
            }),
        )
    add_fieldsets = (
        (None, {
            'fields': ('homework', 'author', 'content', 'upload_date', 'points')
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
                   ('homework', 'author', 'solution', 'content', 'upload_date')
                ),
            }),
        )
    add_fieldsets = (
        (None, {
            'fields': ('homework', 'author', 'solution', 'content', 'upload_date')
        }),
    )


admin.site.register(HomeworkSolution, HomeworkSolutionAdmin)
admin.site.register(HomeworkSolutionHistory, HomeworkSolutionHistoryAdmin)
