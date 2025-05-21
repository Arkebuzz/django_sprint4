from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone

from .forms import CommentForm, PostForm, UserForm
from .models import Category, Post, Comment

User = get_user_model()


def get_all_posts():
    posts = Post.objects.select_related(
        'location', 'author', 'category'
    ).filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=timezone.now()
    )
    return posts


def get_paginator(request, queryset):
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    return posts


# class IndexListView(ListView):
#     template_name = 'blog/index.html'
#     model = Post
#     queryset = model.objects.select_related(
#         'location', 'author', 'category'
#     ).filter(
#         is_published=True,
#         category__is_published=True,
#         pub_date__lte=timezone.now()
#     ).annotate(
#         comment_count=Count('comments')
#     )
#     paginate_by = 10


def index(request):
    posts = get_all_posts().annotate(comment_count=Count('comments'))
    posts = get_paginator(request, posts)
    context = {'page_obj': posts}
    return render(request, 'blog/index.html', context)


# class CategoryListView(ListView):
#     template_name = 'blog/category.html'
#     model = Category
#     paginate_by = 10
#     category = None
#
#     def get_queryset(self):
#         self.category = get_object_or_404(self.model, slug=self.kwargs['slug'], is_published=True)
#         return self.category.posts.select_related(
#             'location', 'author', 'category'
#         ).filter(
#             is_published=True,
#             category__is_published=True,
#             pub_date__lte=timezone.now()
#         ).annotate(
#             comment_count=Count('comments')
#         )
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['category'] = self.category
#         return context


def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug, is_published=True)
    posts = get_all_posts().filter(category=category.id).annotate(
        comment_count=Count('comments')
    )
    posts = get_paginator(request, posts)
    context = {'page_obj': posts, 'category': category}
    return render(request, 'blog/category.html', context)


def post_detail(request, post_id):
    posts = get_all_posts()
    post = get_object_or_404(posts, id=post_id)
    comments = post.comments.select_related('author')
    context = {'post': post, 'comments': comments}
    if request.user.is_authenticated:
        context['form'] = CommentForm()
    return render(request, 'blog/detail.html', context)


def profile_detail(request, username):
    profile = get_object_or_404(User, username=username)
    posts = get_all_posts().filter(author=profile.id).annotate(
        comment_count=Count('comments')
    )
    posts = get_paginator(request, posts)
    context = {'page_obj': posts, 'profile': profile}
    return render(request, 'blog/profile.html', context)


@login_required
def profile_edit(request):
    instance = get_object_or_404(User, username=request.user.username)
    form = UserForm(request.POST or None, instance=instance)
    context = {'form': form}

    if form.is_valid():
        form.save()
        return redirect('blog:profile', request.user.username)

    return render(request, 'blog/user.html', context)


@login_required
def comment_add(request, post_id):
    """Добавление комментария к публикации"""
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('blog:post_detail', post_id)


@login_required
def comment_edit(request, post_id, comment_id):
    instance = get_object_or_404(Comment, pk=comment_id)
    if instance.author != request.user:
        return redirect('blog:post_detail', post_id)

    form = CommentForm(request.POST or None, instance=instance)
    context = {'form': form}

    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', post_id)

    return render(request, 'blog/user.html', context)


@login_required
def comment_delete(request, post_id, comment_id):
    instance = get_object_or_404(Comment, pk=comment_id)
    if instance.author == request.user:
        instance.delete()

    return redirect('blog:post_detail', post_id)
