from django.contrib import admin
from .models import Material


class MaterialAdmin(admin.ModelAdmin):
    model = Material
    ordering = ('date', 'title')
    search_fields = ('date', 'author', 'title')
    list_display = ('date', 'title', 'author')
    list_filter = ('author', )
    fieldsets = (
            (None, {
                "fields": (
                   ('date', 'title', 'author', 'content')
                ),
            }),
        )
    add_fieldsets = (
        (None, {
            'fields':('date', 'title', 'author', 'content')
        }),
    )


admin.site.register(Material, MaterialAdmin)