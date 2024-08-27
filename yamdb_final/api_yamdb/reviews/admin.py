from django.contrib import admin
from .models import Review, Comments


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'title', 'text', 'score', 'pub_date')
    list_filter = ('pub_date',)


class CommentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'review_id', 'text', 'pub_date',)
    list_filter = ('pub_date',)


admin.site.register(Review, ReviewAdmin)
admin.site.register(Comments, CommentsAdmin)
