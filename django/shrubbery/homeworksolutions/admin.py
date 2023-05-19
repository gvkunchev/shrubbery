from django.contrib import admin

from .models import HomeworkSolution


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


admin.site.register(HomeworkSolution, HomeworkSolutionAdmin)
