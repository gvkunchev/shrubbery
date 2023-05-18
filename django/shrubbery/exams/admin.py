from django.contrib import admin
from .models import Exam, ExamResult


class ExamAdmin(admin.ModelAdmin):
    model = Exam
    ordering = ('date', 'title')
    search_fields = ('date', 'title')
    list_display = ('date', 'title')
    list_filter = ('date', )
    fieldsets = (
            (None, {
                "fields": (
                   ('date', 'title')
                ),
            }),
        )
    add_fieldsets = (
        (None, {
            'fields': ('date', 'title')
        }),
    )


class ExamResultAdmin(admin.ModelAdmin):
    model = ExamResult
    ordering = ('exam', 'owner')
    search_fields = ('exam', 'owner')
    list_display = ('exam', 'owner', 'points')
    list_filter = ('exam', 'owner')
    fieldsets = (
            (None, {
                "fields": (
                   ('exam', 'owner', 'points')
                ),
            }),
        )
    add_fieldsets = (
        (None, {
            'fields': ('exam', 'owner', 'points')
        }),
    )


admin.site.register(Exam, ExamAdmin)
admin.site.register(ExamResult, ExamResultAdmin)
