from django.contrib import admin

from .models import Resource


class ResourceAdmin(admin.ModelAdmin):
    model = Resource
    ordering = ('content', )
    search_fields = ('content', )
    list_display = ('content', )
    fieldsets = (
            (None, {
                "fields": (
                   ('content', )
                ),
            }),
        )
    add_fieldsets = (
        (None, {
            'fields': ('content', )
        }),
    )


admin.site.register(Resource, ResourceAdmin)
