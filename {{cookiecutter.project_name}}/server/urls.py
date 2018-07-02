"""
Main URL mapping configuration file.

Include other URLConfs from external apps using method `include()`.

It is also a good practice to keep a single URL to the root index page.

This examples uses Django's default media
files serving technique in development.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.contrib import admin
from django.urls import include, re_path
from django.views.generic import TemplateView

from server.main_app import urls as main_urls
from server.main_app.views import index

admin.autodiscover()


urlpatterns = [
    # django-admin:
    re_path(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    re_path(r'^admin/', admin.site.urls),

    # Apps:
    re_path(r'^main/', include(main_urls)),

    # Text and xml static files:
    re_path(r'^robots\.txt$', TemplateView.as_view(
        template_name='txt/robots.txt',
        content_type='text/plain',
    )),
    re_path(r'^humans\.txt$', TemplateView.as_view(
        template_name='txt/humans.txt',
        content_type='text/plain',
    )),

    # It is a good practice to have explicit index view:
    re_path(r'^$', index, name='index'),
]

if settings.DEBUG:
    import debug_toolbar
    from django.views.static import serve

    urlpatterns = [
        # URLs specific only to django-debug-toolbar:
        re_path(r'^__debug__/', include(debug_toolbar.urls)),

        # Serving media files in development only:
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ] + urlpatterns

# Customize default error views:
# https://docs.djangoproject.com/en/1.11/topics/http/views/#customizing-error-views

# handler400 = 'your_app.views.error_handler'
# handler403 = 'your_app.views.error_handler'
# handler404 = 'your_app.views.error_handler'
# handler500 = 'your_app.views.error_handler'
