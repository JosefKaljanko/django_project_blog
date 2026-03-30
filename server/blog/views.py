from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404    # redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required       # log_req

from .forms import PostForm     #
from .models import Post


#   ╔════════════════════════════════════════════════╗
#   ║           FVB - Function Base View             ║
#   ╚════════════════════════════════════════════════╝
def post_list(request):
    """FVB - Function Base View

    Zobrazí všechny posty které mají status Published
    """

    posts = Post.objects.filter(status=Post.Status.PUBLISHED).order_by("-published_at", "-created_at")
    messages.info(request, "Toto je view FVB")
    return render(request, "blog/post_list.html", {"posts": posts})

def post_detail(request, slug):
    """FVB - Function Base View

    Zobrazí Detail postu které mají status Published
    """
    post = get_object_or_404(Post, slug=slug, status=Post.Status.PUBLISHED)
    messages.info(request, "Toto je view FVB")
    return render(request, "blog/post_detail.html", {"post": post})




#   ╔════════════════════════════════════════════════╗
#   ║            CVB - Class Base View               ║
#   ╚════════════════════════════════════════════════╝

from django.views.generic import ListView, DetailView
class PostListView(ListView):
    """CVB - Class Base View

    Zobrazí všechny Posty které mají status Published
    """
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    # messages.info = "Toto je view CVB"

    def get_queryset(self):
        return (
            Post.objects
            .filter(status=Post.Status.PUBLISHED)
            .order_by("-published_at", "-created_at")
        )

    def get(self, request, *args, **kwargs):
        messages.info(request, "Toto je view CVB")
        # return super(PostListView, self).get(request, *args, **kwargs)
        return super().get(request, *args, **kwargs)

class PostDetailView(DetailView):
    """CVB - Class Base View"""
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"
    slug_field = "slug"
    slug_url_kwarg = "slug"
    # messages.success = "Toto je view CVB"
    def get_queryset(self):
        return Post.objects.filter(status=Post.Status.PUBLISHED)

    def get(self,request,*args, **kwargs):
        messages.info(request, "Toto je view CVB")
        return super().get(request, *args, **kwargs)

from django.views import View

# class NewView(View):
#     def get(self,request):
#         ...
#
#     def post(self,request):
#         ...
#
#     def put(self,request):
#         ...
#
#     def delete(self,request):
#         ...


#   ╔════════════════════════════════════════════════╗
#   ║          FVB - Funcional Base View             ║
#   ║              pozdeji předěláme                 ║
#   ║        importy: redirect, login_required       ║
#   ║              PostForm, timezone                ║
#   ╚════════════════════════════════════════════════╝

@login_required
def post_create(request):
    # print("METHOD:", request.method)
    if request.method == "POST":
        # print("POST DATA:", dict(request.POST))
        form = PostForm(request.POST)
        # print("FORM VALID:", form.is_valid())
        if form.is_valid():
            post = form.save(commit=False)      # neukládat do DB
            # print("POST (BEFORE SAVE):", post, "AUTHOR:", request.user)
            post.author = request.user          # doplnění autora
            if post.status == Post.Status.PUBLISHED and post.published_at is None:
                post.published_at = timezone.now()
            post.save()                         # až teď uložíme
            # print("POST SAVED ID:", post.id)
            messages.success(request, "Článek byl vytvořen...")
            return redirect("blog:post_detail", slug=post.slug)
    else:
        form = PostForm()
    return render(request, "blog/post_form.html", {"form": form, "mode": "create"})

@login_required
def post_update(request, slug: str):
    post = get_object_or_404(Post, slug=slug, author=request.user)      # autor muze editovat jen své

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)        # instance=post ??
        if form.is_valid():
            post = form.save(commit=False)
            if post.status == Post.Status.PUBLISHED and post.published_at is None:
                post.published_at = timezone.now()
            post.save()
            messages.success(request, "Článek byl upraven...")
            return redirect("blog:post_detail", slug=post.slug)
    else:
        form = PostForm(instance=post)

    return render(request, "blog/post_form.html", {"form": form, "mode": "update", "post": post})








