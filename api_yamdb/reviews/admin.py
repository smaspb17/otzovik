from django.contrib import admin

from .models import Comment, Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'score',)
    search_fields = ('text',)

    
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('title', 'review', 'text',)
    search_fields = ('text',)
