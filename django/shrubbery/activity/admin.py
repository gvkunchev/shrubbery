from django.contrib import admin
from .models import Action


class ActionAdmin(admin.ModelAdmin):
    model = Action
    ordering = ('date', )
    search_fields = ('date', 'author', 'type')
    list_display = ('date', 'author', 'type', 'link')
    list_filter = ('date', 'author', 'type')
    fieldsets = (
            (None, {
                "fields": (
                   ('date', 'author', 'type', 'link')
                ),
            }),
        )
    add_fieldsets = (
        (None, {
            'fields': ('date', 'author', 'type', 'link')
        }),
    )


admin.site.register(Action, ActionAdmin)
