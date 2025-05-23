from django.urls import path

from . import views

app_name = 'blog'

urls_pages = [
    path('', views.index, name='index'),
    path(
        'category/<slug:slug>/', views.category_posts, name='category_posts'
    ),
]

urls_post = [
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('posts/<int:post_id>/edit/', views.post_edit, name='edit_post'),
    path('posts/<int:post_id>/delete/', views.post_delete, name='delete_post'),
    path('posts/create/', views.post_create, name='create_post'),
]

urls_comment = [
    path(
        'posts/<int:post_id>/comment/', views.comment_add, name='add_comment'
    ),
    path(
        'posts/<int:post_id>/delete_comment/<int:comment_id>/',
        views.comment_delete, name='delete_comment'
    ),
    path(
        'posts/<int:post_id>/edit_comment/<int:comment_id>',
        views.comment_edit, name='edit_comment'
    ),
]

urls_profile = [
    path('profile/<username>/', views.profile_detail, name='profile'),
    path('profile/edit', views.profile_edit, name='edit_profile'),
]

urlpatterns = urls_pages + urls_post + urls_comment + urls_profile
