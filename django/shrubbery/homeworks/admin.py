from django.contrib import admin

from .models import Homework, HomeworkComment


class HomeworkAdmin(admin.ModelAdmin):
    model = Homework
    ordering = ('creation_date', 'title', 'author')
    search_fields = ('creation_date', 'title', 'title', 'author')
    list_display = ('title', 'creation_date', 'deadline', 'author')
    list_filter = ('hidden', 'verified')
    fieldsets = (
            (None, {
                "fields": (
                   ('title', 'content', 'creation_date', 'author',
                    'deadline', 'points', 'sanity_test', 'full_test',
                    'custom_module_name', 'custom_module_content',
                    'hidden', 'verified', 'executing_tests')
                ),
            }),
        )
    add_fieldsets = (
        (None, {
            'fields': ('title', 'content', 'creation_date', 'author',
                       'deadline', 'points', 'sanity_test', 'full_test',
                       'custom_module_name', 'custom_module_content',
                       'hidden', 'verified', 'executing_tests')
        }),
    )


class HomeworkCommentAdmin(admin.ModelAdmin):
    model = HomeworkComment
    ordering = ('date', 'author')
    search_fields = ('date', 'author', 'homework', 'parent', 'content')
    list_display = ('date', 'author', 'homework')
    list_filter = ('author', 'homework')
    fieldsets = (
            (None, {
                "fields": (
                   ('date', 'author', 'homework', 'parent', 'content', 'starred')
                ),
            }),
        )
    add_fieldsets = (
        (None, {
            'fields': ('date', 'author', 'homework', 'parent', 'content', 'starred')
        }),
    )

admin.site.register(Homework, HomeworkAdmin)
admin.site.register(HomeworkComment, HomeworkCommentAdmin)
