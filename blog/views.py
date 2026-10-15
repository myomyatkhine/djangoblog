from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView
)
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth import login
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)

from .models import Post, Category
from .forms import PostForm, RegisterForm
from django.contrib import messages

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"
    login_url = "login"

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Post published successfully!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("post_detail", kwargs={"slug": self.object.slug})

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "blog/register.html"
    success_url = "/"

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"
    login_url = "login"

    def test_func(self):
        return self.get_object().author == self.request.user

    def get_success_url(self):
        return reverse_lazy(
            "post_detail",
            kwargs={"slug": self.object.slug}
        )


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    login_url = "login"
    success_url = reverse_lazy("home")

    def test_func(self):
        return self.get_object().author == self.request.user


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"
    login_url = "login"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "post_detail",
            kwargs={"slug": self.object.slug}
        )


class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    paginate_by = 6

    def get_queryset(self):
        return Post.objects.filter(
            status="published"
        ).order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        qs = Post.objects.filter(status="published")

        if self.request.user.is_authenticated:
            qs = Post.objects.filter(
                Q(status="published") | Q(author=self.request.user)
            )

        return qs


class MyPostsView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "blog/my_posts.html"
    paginate_by = 6
    login_url = "login"

    def get_queryset(self):
        return Post.objects.filter(
            author=self.request.user
        ).order_by("-created_at")


def about(request):
    return render(
        request,
        "blog/about.html",
        {"team": "DjangoBlog Team"}
    )


def contact(request):
    return render(
        request,
        "blog/contact.html"
    )


def custom_403(request, exception=None):
    return render(
        request,
        "blog/403.html",
        status=403
    )
class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    paginate_by = 6

    def get_queryset(self):
        qs = Post.objects.filter(status="published").order_by("-created_at")
        category_slug = self.request.GET.get("category")
        if category_slug:
            qs = qs.filter(category__name__iexact=category_slug)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context