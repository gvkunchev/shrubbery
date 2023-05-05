from django.contrib import admin
from .models import NewsArticle


class NewsArticleAdmin(admin.ModelAdmin):
    model = NewsArticle
    ordering = ('date', 'author')
    search_fields = ('date', 'author', 'title', 'content')
    list_display = ('date', 'author', 'title')
    list_filter = ('author', )
    fieldsets = (
            (None, {
                "fields": (
                   ('date', 'author', 'title', 'content')
                ),
            }),
        )
    add_fieldsets = (
        (None, {
            'fields': ('date', 'author', 'title', 'content')
        }),
    )


admin.site.register(NewsArticle, NewsArticleAdmin)