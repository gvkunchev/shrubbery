from django.contrib.auth.models import Group
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Student, Teacher


class StudentAdmin(UserAdmin):
    model = Student
    ordering = ('fn', 'email')
    search_fields = ('fn', 'email', 'first_name', 'last_name')
    list_display = ('fn', 'email', 'first_name', 'last_name', 'is_active')
    list_filter = ('is_active', )
    fieldsets = (
            (None, {
                "fields": (
                    ('image', 'fn', 'email', 'first_name', 'last_name', 'github', 'dark_theme', 'is_active',
                     'email_notification_news', 'email_notification_forum', 'email_notification_homework', 'email_notification_challenge',
                     'email_notification_solution_comments')
                ),
            }),
        )
    add_fieldsets = (
        (None, {
            'fields': ('fn', 'email', 'first_name', 'last_name',
                       'image', 'github', 'dark_theme',
                       'password1', 'password2', 'is_active')
        }),
    )


class TeacherAdmin(UserAdmin):
    model = Teacher
    ordering = ('email',)
    search_fields = ('email', 'first_name', 'last_name')
    list_display = ('email', 'first_name', 'last_name', 'is_active')
    list_filter = ('is_active', )
    fieldsets = (
            (None, {
                "fields": (
                    ('image', 'email', 'first_name', 'last_name', 'github', 'dark_theme', 'is_active',
                     'email_notification_news', 'email_notification_forum', 'email_notification_homework', 'email_notification_challenge',
                     'email_notification_solution_comments')
                ),
            }),
        )
    add_fieldsets = (
        (None, {
            'fields': ('email', 'first_name', 'last_name',
                       'image', 'github', 'dark_theme',
                       'password1', 'password2', 'is_active')
        }),
    )


admin.site.register(Student, StudentAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.unregister(Group)