from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render, redirect

from .forms import PostForm
from .models import Group, Post, User

NMB_PUB = 10


def paginator(request, posts):
    page_number = request.GET.get('page')
    page_obj = Paginator(posts, NMB_PUB).get_page(page_number)
    return page_obj


def index(request):
    posts = Post.objects.order_by('-pub_date')
    page_obj = paginator(request, posts)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).order_by('-pub_date')
    page_obj = paginator(request, posts)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = author.posts.all().order_by('-pub_date')
    post_count = posts.count()
    page_obj = paginator(request, posts)
    context = {
        'author': author,
        'page_obj': page_obj,
        'post_count': post_count,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    author = post.author
    author_posts = author.posts
    post_count = author_posts.count()
    context = {
        'title': post.text,
        'post': post,
        'post_count': post_count,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:profile', username=post.author)
        return render(request, 'posts/create_post.html', {'form': form})
    form = PostForm()
    return render(request, 'posts/create_post.html', {'form': form})


def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    is_edit = True
    if request.user == post.author:
        if request.method == 'POST':
            form = PostForm(request.POST or None, instance=post)
            if form.is_valid():
                post = form.save()
                return redirect('posts:post_detail', post.pk)
            return render(request, 'posts/update_post.html',
                          {'form': form, 'is_edit': is_edit, 'post': post})
        form = PostForm(instance=post)
        return render(request, 'posts/update_post.html',
                      {'form': form, 'is_edit': is_edit, 'post': post})
    else:
        return redirect('posts:post_detail', post.pk)
