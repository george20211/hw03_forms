from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator
from django.views.generic.base import TemplateView
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from .models import Group, Post, User


def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, "index.html", {'page': page, })


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()[:12]
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, "group.html", {"group": group,
                  'page': page})


class JustStaticPage(TemplateView):
    template_name = 'just_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['just_title'] = 'Очень простая страница'
        context['just_text'] = 'я молодец'
        return context


def profile(request, username):
    profile = get_object_or_404(User, username=username)
    author_posts = profile.posts.all()
    paginator = Paginator(author_posts, 5)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        "page": page,
        "profile": profile,
    }
    return render(request, 'profile.html', context)


def post_view(request, username, post_id):
    post = get_object_or_404(Post, author__username=username, id=post_id)
    context = {
        "author_posts": post.author,
        "post": post
    }
    return render(request, 'post.html', context)


@login_required
def new_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('index')
    form = PostForm()
    return render(request, 'new.html', {'form': form})


@login_required
def post_edit(request, username, post_id):
    error1 = "Вы не автор поста"
    post = get_object_or_404(Post, author__username=username, id=post_id)
    form = PostForm(request.POST,
                    instance=post)
    if request.user == post.author:
        if request.method == 'POST' or None:
            if form.is_valid():
                form.save()
                return redirect("post", username, post_id)
        form = PostForm(instance=post)
        return render(request, "new.html", {"form": form})
    return render(request, 'error.html', {"error1": error1})


def stats(request):
    post_count_all = len(Post.objects.all())
    users_count_all = len(User.objects.all())
    last_register = User.date_joined
    context = {
        'post_count_all': post_count_all,
        'users_count_all': users_count_all,
        'last_register': last_register,
    }
    return render(request, 'top.html', context)
