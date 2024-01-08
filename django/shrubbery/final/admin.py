from django.contrib import admin

from .models import FinalScheduleSlot, FinalExchange


class FinalScheduleSlotAdmin(admin.ModelAdmin):
    model = FinalScheduleSlot
    ordering = ('start', 'end')
    search_fields = ('start', 'end', 'students')
    list_display = ('start', 'end')
    fieldsets = (
            (None, {
                "fields": (
                   ('start', 'end', 'students')
                ),
            }),
        )
    add_fieldsets = (
        (None, {
            'fields': ('start', 'end', 'students')
        }),
    )


class FinalExchangeAdmin(admin.ModelAdmin):
    model = FinalExchange
    ordering = ('requester', 'confirmer')
    search_fields = ('requester', 'confirmer')
    list_display = ('requester', 'confirmer')
    fieldsets = (
            (None, {
                "fields": (
                   ('requester', 'confirmer')
                ),
            }),
        )
    add_fieldsets = (
        (None, {
            'fields': ('requester', 'confirmer')
        }),
    )


admin.site.register(FinalScheduleSlot, FinalScheduleSlotAdmin)
admin.site.register(FinalExchange, FinalExchangeAdmin)
