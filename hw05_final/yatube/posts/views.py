from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import HttpResponse, get_object_or_404, redirect, render

from .forms import PostForm, CommentForm
from .models import Group, Post, User, Comment, Follow

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
    following = False
    if (request.user.is_authenticated and Follow.objects.filter(
            author=author.id, user=request.user.id).exists()):
        following = True
    posts = author.posts.all().order_by('-pub_date')
    post_count = posts.count()
    page_obj = paginator(request, posts)
    context = {
        'author': author,
        'page_obj': page_obj,
        'post_count': post_count,
        'following': following,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    author = post.author
    author_posts = author.posts
    post_count = author_posts.count()
    comments = Comment.objects.filter(post=post_id)
    form = CommentForm(request.POST or None)
    context = {
        'title': post.text,
        'post': post,
        'post_count': post_count,
        'comments': comments,
        'form': form,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST or None, files=request.FILES or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:profile', username=post.author)
        return render(request, 'posts/create_post.html', {'form': form})
    form = PostForm()
    return render(request, 'posts/create_post.html', {'form': form})


def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        return redirect('posts:post_detail', post_id=post_id)

    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post
    )
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id=post_id)
    context = {
        'post': post,
        'form': form,
        'is_edit': True,

    }
    return render(request, 'posts/create_post.html', context)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    posts = Post.objects.filter(
        author__following__user=request.user).order_by('-pub_date')
    paginator = Paginator(posts, NMB_PUB)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "posts/follow.html",
                  {"page_obj": page_obj})

def not_follow(request):
    return render(request, 'posts/not_follow.html')

@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    if request.user != author:
        Follow.objects.get_or_create(user=request.user, author=author)
        return redirect('posts:follow_index')
    else:
        return redirect('posts:not_follow')


@login_required
def profile_unfollow(request, username):
    follow_user = get_object_or_404(User, username=username)
    Follow.objects.filter(user=request.user, author=follow_user).delete()
    return redirect('posts:follow_index')
