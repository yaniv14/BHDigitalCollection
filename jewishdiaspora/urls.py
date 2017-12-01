from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.views.i18n import JavaScriptCatalog
from django.views.static import serve

from artifacts import views

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('authtools.urls')),
    url(r'^jsi18n/$', JavaScriptCatalog.as_view(packages=['artifacts']), name='javascript-catalog'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^uploads/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
        url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT})
    ]
