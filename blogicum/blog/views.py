from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone

from .forms import CommentForm, PostForm, UserForm
from .models import Category, Post, Comment

User = get_user_model()


def get_all_posts(default_filter=True, comments=True, **kwargs):
    """Получение списка постов."""
    if default_filter:
        kwargs |= {
            'is_published': True,
            'category__is_published': True,
            'pub_date__lte': timezone.now()
        }

    posts = Post.objects.select_related(
        'location', 'author', 'category'
    ).filter(**kwargs).order_by('-pub_date')

    if comments:
        posts = posts.annotate(comment_count=Count('comments'))

    return posts


def get_paginator(request, queryset):
    """Использование пагинатора."""
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    return posts


def index(request):
    """Главная страница."""
    posts = get_all_posts()
    posts = get_paginator(request, posts)
    context = {'page_obj': posts}
    return render(request, 'blog/index.html', context)


def category_posts(request, slug):
    """Страница категории."""
    category = get_object_or_404(Category, slug=slug, is_published=True)
    posts = get_all_posts(category=category.id)
    posts = get_paginator(request, posts)
    context = {'page_obj': posts, 'category': category}
    return render(request, 'blog/category.html', context)


def post_detail(request, post_id):
    """Страница поста."""
    post = get_object_or_404(Post, pk=post_id)

    if request.user != post.author and not (
            post.is_published
            and post.category.is_published
            and post.pub_date < timezone.now()
    ):
        raise Http404

    comments = post.comments.select_related('author')
    context = {'post': post, 'comments': comments}

    if request.user.is_authenticated:
        context['form'] = CommentForm()

    return render(request, 'blog/detail.html', context)


@login_required
def post_create(request):
    """Создание поста."""
    form = PostForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('blog:profile', request.user.username)

    context = {'form': form}
    return render(request, 'blog/create.html', context)


@login_required
def post_edit(request, post_id):
    """Редактирование поста."""
    post = get_object_or_404(Post, pk=post_id)

    if post.author != request.user:
        return redirect('blog:post_detail', post.id)

    form = PostForm(
        request.POST or None,
        request.FILES or None,
        instance=post
    )

    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', post.id)

    context = {'form': form}
    return render(request, 'blog/create.html', context)


@login_required
def post_delete(request, post_id):
    """Удаление поста."""
    post = get_object_or_404(Post, id=post_id)

    if request.user != post.author:
        return redirect('blog:post_detail', post_id)

    form = PostForm(request.POST or None, instance=post)
    if request.method == 'POST':
        post.delete()
        return redirect('blog:index')

    context = {'form': form}
    return render(request, 'blog/create.html', context)


def profile_detail(request, username):
    """Страница профиля пользователя."""
    profile = get_object_or_404(User, username=username)

    if profile == request.user:
        posts = get_all_posts(default_filter=False, author=profile.id)
    else:
        posts = get_all_posts(author=profile.id)

    posts = get_paginator(request, posts)
    context = {'page_obj': posts, 'profile': profile}
    return render(request, 'blog/profile.html', context)


@login_required
def profile_edit(request):
    """Изменение профиля."""
    profile = get_object_or_404(User, username=request.user.username)

    if request.user != profile:
        return redirect('blog:profile', profile.username)

    form = UserForm(request.POST or None, instance=profile)

    if form.is_valid():
        form.save()
        return redirect('blog:profile', request.user.username)

    context = {'form': form}
    return render(request, 'blog/user.html', context)


@login_required
def comment_add(request, post_id):
    """Добавление комментария."""
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()

    return redirect('blog:post_detail', post_id)


@login_required
def comment_edit(request, post_id, comment_id):
    """Изменения комментария."""
    comment = get_object_or_404(Comment, pk=comment_id)

    if comment.author != request.user:
        return redirect('blog:post_detail', post_id)

    form = CommentForm(request.POST or None, instance=comment)

    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', post_id)

    context = {'form': form}
    return render(request, 'blog/user.html', context)


@login_required
def comment_delete(request, post_id, comment_id):
    """Удаление комментария."""
    comment = get_object_or_404(Comment, pk=comment_id)

    if comment.author != request.user:
        return redirect('blog:post_detail', post_id)

    if request.method == 'POST':
        comment.delete()
        return redirect('blog:post_detail', post_id)

    context = {'comment': comment}
    return render(request, 'blog/comment.html', context)
