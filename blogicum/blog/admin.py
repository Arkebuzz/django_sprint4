from django.contrib import admin

from .models import Category, Location, Post, Comment


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'slug',
        'is_published',
        'description',
        'created_at',
    )
    list_editable = (
        'slug',
        'is_published',
    )
    search_fields = (
        'title',
        'slug',
    )
    list_filter = (
        'is_published',
    )


class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'is_published',
        'created_at',
    )
    list_editable = (
        'is_published',
    )
    search_fields = (
        'name',
    )
    list_filter = (
        'is_published',
    )


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'author',
        'location',
        'category',
        'text',
        'is_published',
        'pub_date',
        'created_at',
    )
    list_editable = (
        'is_published',
    )
    search_fields = (
        'title',
        'author',
        'location',
        'category',
    )
    list_filter = (
        'is_published',
        'location',
        'category',
    )
    list_display_links = (
        'author',
        'location',
        'category',
    )


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'post',
        'text',
        'author',
        'created_at',
    )
    list_editable = (
    )
    search_fields = (
        'post',
        'author',
    )
    list_filter = (
    )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
