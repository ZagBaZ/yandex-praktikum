from django.contrib import admin

from .models import Genre, Title, Category, GenreTitle


class TitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'year', 'description',)
    search_fields = ('name',)
    list_filter = ('year', 'genre')
    empty_value_display = '-пусто-'


admin.site.register(Title, TitleAdmin)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(GenreTitle)
