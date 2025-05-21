from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path(
        'category/<slug:slug>/', views.category_posts, name='category_posts'
    ),

    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('posts/<int:post_id>/edit/', lambda x, y: None, name='edit_post'),
    path('posts/create/', lambda: None, name='create_post'),

    path('posts/<int:post_id>/comment/', views.comment_add, name='add_comment'),
    path(
        'posts/<int:post_id>/delete_comment/<int:comment_id>/',
        views.comment_delete, name='delete_comment'
    ),
    path(
        'posts/<int:post_id>/edit_comment/<int:comment_id>',
        views.comment_edit, name='edit_comment'
    ),

    path('profile/<username>/', views.profile_detail, name='profile'),
    path('profile/edit', views.profile_edit, name='edit_profile'),
]
