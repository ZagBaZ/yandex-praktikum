from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'email',
        'first_name',
        'last_name',
        'bio',
        'is_superuser',
        'is_staff',
        'role'
    )
    search_fields = ('username',)
    list_editable = ('bio', 'is_superuser', 'is_staff', 'role')
    list_filter = ('username',)
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)
