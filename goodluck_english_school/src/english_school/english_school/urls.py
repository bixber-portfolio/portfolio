from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from . import views

handler403 = 'pages.views.permission_denied'
handler404 = 'pages.views.page_not_found'
handler500 = 'pages.views.server_error'

urlpatterns = [
    path('', views.HomePage.as_view(), name='homepage'),
    path('pages/', include('pages.urls')),
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls')),
    path('accounts/', include('profiles.urls')),
    path('services/', include('services.urls')),
    path('payments/', include('payments.urls')),
    path('orders/', include('orders.urls')),
    path('lessons/', include('lessons.urls')),
    path('news/', include('news.urls')),
]

# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
