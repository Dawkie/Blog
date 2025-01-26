from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404

from .forms import PostForm
from .models import Post


@login_required
def posts_list(request):

    posts = Post.objects.filter(status="published")

    page_number = request.GET.get("page", 1)
    per_page = request.GET.get("per_page", 10)
    paginator = Paginator(posts, per_page)

    page_obj = paginator.page(page_number)

    return render(request, "list.html", {"page_obj": page_obj})


@login_required
def post_details(request, post_id):
    form = None
    post = get_object_or_404(Post, id=post_id, status="published")

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()

    if request.user == post.author:
        form = PostForm(instance=post)

    return render(request, "details.html", {"post": post, "form": form})


@login_required
def post_create(request):
    form = PostForm()
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            if request.user.is_superuser:
                post.status = "published"
            post.save()
            return redirect("Posts:list")
    return render(request, "create.html", {"form": form})






def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("Posts:list")
    else:
        form = AuthenticationForm()

    return render(request, "login.html", {"form": form})