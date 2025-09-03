from django.urls import path

from . import views

app_name = 'news'

urlpatterns = [
    path('all', views.NewsList.as_view(), name='news_list'),
    path('<news_id>/detail', views.NewsDetail.as_view(), name='news_detail'),
]