from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect

from .models import Post


class CommentRedirectMixin:
    def dispatch(self, request, *args, **kwargs):
        self.blog = get_object_or_404(Post, pk=kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.post = self.blog
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'post_id': self.blog.id})


class PermissionMixin:
    def dispatch(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['post_id'])
        if post.author != request.user:
            return HttpResponseRedirect(
                reverse_lazy('blog:post_detail', kwargs={'post_id': post.pk})
            )
        return super().dispatch(request, *args, **kwargs)
