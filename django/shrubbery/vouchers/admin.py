from django.contrib import admin

from .models import Voucher


class VoucherAdmin(admin.ModelAdmin):
    model = Voucher
    ordering = ('token', )
    search_fields = ('owner', 'token', 'date')
    list_display = ('token', 'owner', 'date', 'points')
    list_filter = ('owner', 'date')
    fieldsets = (
            (None, {
                "fields": (
                   ('owner', 'token', 'points', 'date')
                ),
            }),
        )
    add_fieldsets = (
        (None, {
            'fields': ('owner', 'token', 'points', 'date')
        }),
    )


admin.site.register(Voucher, VoucherAdmin)
