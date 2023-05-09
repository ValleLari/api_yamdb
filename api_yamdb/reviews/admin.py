from django.contrib import admin
from reviews.models import Title


class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'category', 'name', 'year', 'description')
    list_display_links = ('name', 'description')
    list_editable = ('category',)
    list_filter = ('genre', 'category')
    empty_value_display = '-пусто-'
    search_fields = ('name',)


admin.site.register(Title, TitleAdmin)
