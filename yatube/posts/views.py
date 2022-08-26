from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from .forms import PostForm
from .models import Post, Group, User
from .utils import paginate


def index(request):
    """Возвращает главную страницу"""
    posts = Post.objects.select_related('author').all()
    context = {
        'page_obj': paginate(posts, request),
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    """Возвращает страницу групп"""
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.select_related()
    context = {
        'group': group,
        'page_obj': paginate(posts, request),
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    """Возвращает профайл пользователя"""
    author = get_object_or_404(User, username=username)
    posts = author.posts.select_related('author').all()
    context = {
        'author': author,
        'page_obj': paginate(posts, request),
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    """Возвращает детальную информацию о посте"""
    post = get_object_or_404(
        Post.objects.select_related('author', 'group'),
        pk=post_id)
    context = {
        'post': post,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    """Возвращает  создание поста, для залогиненного пользователя"""
    form = PostForm(request.POST or None,
                    files=request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:profile', post.author)
    return render(request, 'posts/create_post.html', {'form': form})


@login_required
def post_edit(request, post_id):
    """Возвращает редактирование поста, для залогиненного
    автора поста или предлагает создать пост"""
    post = get_object_or_404(Post, pk=post_id)
    is_edit = True
    if request.user != post.author:
        return redirect('posts:post_detail', post.id)
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post)
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id)
    form = PostForm(instance=post)
    return render(request, 'posts/create_post.html', {
        'post': post, 'form': form, 'is_edit': is_edit
    })
