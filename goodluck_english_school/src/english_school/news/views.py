from datetime import datetime

from django.views.generic import ListView, DetailView

from .models import News


class NewsList(ListView):
    model = News
    template_name = 'news/news_list.html'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now_date'] = datetime.now().date()
        return context


class NewsDetail(DetailView):
    model = News
    template_name = 'news/news_detail.html'
    pk_url_kwarg = 'news_id'
    context_object_name = 'obj'
