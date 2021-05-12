from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator
from django.views.generic.base import TemplateView
from .forms import PostForm
from django.contrib.auth.decorators import login_required

from .models import Group, Post, User
import datetime as dt
from django.contrib.auth import get_user_model


def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    latest = Post.objects.all()[:11]
    return render(request, "index.html", {'page': page, })


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()[:12]
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        "group": group,
        "posts": posts,
        "page": page
    }
    return render(request, "group.html", context)


class JustStaticPage(TemplateView):
    template_name = 'just_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['just_title'] = 'Очень простая страница'
        context['just_text'] = '5 мин на страницу!'
        return context


def profile(request, username):
    profile = get_object_or_404(User, username=username)
    author_post = Post.objects.filter(author__username=username)
    paginator = Paginator(author_post, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        "username": username,
        "profile": profile,
        "author_post": author_post,
        "page": page,
    }
    return render(request, 'profile.html', context)


def post_view(request, username, post_id):
    post = get_object_or_404(Post, pk=post_id, author__username=username)
    return render(
        request, 'post.html',
        {'post': post,
         'author': post.author})


@login_required
def new_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("index")
        return render(request, 'news.html', {'form': form})
    form = PostForm()
    return render(request, 'news.html', {'form': form})


@login_required
def post_edit(request, username, post_id):
    if request.user == User.objects.get(username=username):
        post = Post.objects.get(id=post_id)
        if request.method == 'POST':
            form = PostForm(request.POST,
                            instance=post)
            if form.is_valid():
                form.save()
                return redirect("post", username, post_id)
            return render(request, "news.html", {"form": form})
        form = PostForm(instance=post)
        return render(request, 'news.html', {'form': form, 'post': post})
    return redirect('post', username=username, post_id=post_id)
