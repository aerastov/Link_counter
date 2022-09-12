from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

urlpatterns = [
    path('visited_domains', visited_domains, name='domains'),
    path('visited_links', visited_links, name="links"),
]