from django.urls import re_path

from server.main_app.views import index

# Place your URLs here:

urlpatterns = [
    re_path(r'^hello/$', index, name='hello'),
]
