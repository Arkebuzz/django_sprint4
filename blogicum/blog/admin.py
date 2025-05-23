from django.contrib import admin

from .models import Category, Location, Post, Comment


@admin.register(Category)
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


@admin.register(Location)
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


@admin.register(Post)
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


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'post',
        'text',
        'author',
        'created_at',
    )
