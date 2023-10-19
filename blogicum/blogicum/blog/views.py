import datetime as dt

from django.views.generic import (
    DetailView, ListView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect

from .models import Category, Post, Comment, User
from .forms import PostForm, CommentForm, ProfileForm
from .mixins import CommentRedirectMixin, PermissionMixin


class PostListView(ListView):
    model = Post
    ordering = '-pub_date'
    paginate_by = 10
    template_name = 'blog/index.html'
    queryset = Post.objects.select_related(
        'category',
        'location',
        'author',
    ).filter(
        category__is_published=True,
        is_published=True,
        pub_date__lte=dt.datetime.now().date(),
    )


class CategoryPostListView(ListView):
    model = Post
    ordering = '-pub_date'
    paginate_by = 10
    template_name = 'blog/category.html'

    def dispatch(self, request, *args, **kwargs):
        self.category = get_object_or_404(
            Category,
            slug=kwargs['category_slug'],
            is_published=True,
        )
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.category
        return context

    def get_queryset(self):
        query = Post.objects.select_related(
            'category',
            'location',
            'author',
        ).filter(
            category_id=self.category.id,
            is_published=True,
            pub_date__lte=dt.datetime.now().date(),
        )
        return query


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = (
            self.object.comments.select_related('author')
        )
        return context


class ProfileDetailView(DetailView):
    model = User
    template_name = 'blog/profile.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = Post.objects.filter(author=self.object.id)
        hey = Paginator(query, 10)
        page_number = self.request.GET.get('page')
        page_obj = hey.get_page(page_number)
        context["page_obj"] = page_obj
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'blog/user.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def dispatch(self, request, *args, **kwargs):
        get_object_or_404(User, username=request.user, is_active=True)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('blog:profile', kwargs={'username': self.request.user})


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:profile', kwargs={'username': self.request.user})


class PostUpdateView(PermissionMixin, LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def get_success_url(self) -> str:
        return reverse('blog:post_detail', kwargs={'post_id': self.object.pk})


class PostDeleteView(PermissionMixin, LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')
    pk_url_kwarg = 'post_id'


class CommentCreateView(LoginRequiredMixin, CommentRedirectMixin, CreateView):
    blog = None
    model = Comment
    form_class = CommentForm


class CommentUpdateView(LoginRequiredMixin, CommentRedirectMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

    def dispatch(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['post_id'])
        comment = get_object_or_404(Comment, pk=kwargs['comment_id'])
        if request.user != comment.author:
            return HttpResponseRedirect(
                reverse_lazy('blog:post_detail', kwargs={'post_id': post.pk})
            )
        return super().dispatch(request, *args, **kwargs)


class CommentDeleteView(LoginRequiredMixin, CommentRedirectMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

    def dispatch(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['post_id'])
        comment = get_object_or_404(Comment, pk=kwargs['comment_id'])
        if request.user != comment.author:
            return HttpResponseRedirect(
                reverse_lazy('blog:post_detail', kwargs={'post_id': post.pk})
            )
        return super().dispatch(request, *args, **kwargs)
