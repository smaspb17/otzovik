from django.contrib import admin

from .models import Comment, Review


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'score',)
    search_fields = ('text',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('title', 'review', 'text',)
    search_fields = ('text',)


admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
