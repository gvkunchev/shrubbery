from django.contrib import admin

from .models import KingArthur, SirBedevere


class KingArthurAdmin(admin.ModelAdmin):
    model = KingArthur
    ordering = ('owner', )
    search_fields = ('owner', 'points', 'achieved')
    list_display = ('owner', 'points', 'achieved')
    list_filter = ('owner', 'points', 'achieved')
    fieldsets = (
            (None, {
                "fields": (
                   ('owner', 'points', 'achieved')
                ),
            }),
        )
    add_fieldsets = (
        (None, {
            'fields': ('owner', 'points', 'achieved')
        }),
    )


class SirBedevereAdmin(admin.ModelAdmin):
    model = SirBedevere
    ordering = ('owner', )
    search_fields = ('owner', 'points', 'achieved')
    list_display = ('owner', 'points', 'achieved')
    list_filter = ('owner', 'points', 'achieved')
    fieldsets = (
            (None, {
                "fields": (
                   ('owner', 'points', 'achieved')
                ),
            }),
        )
    add_fieldsets = (
        (None, {
            'fields': ('owner', 'points', 'achieved')
        }),
    )

admin.site.register(KingArthur, KingArthurAdmin)
admin.site.register(SirBedevere, SirBedevereAdmin)
