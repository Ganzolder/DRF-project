# apidocs/urls.py
from rest_framework.documentation import include_docs_urls
from django.urls import path

urlpatterns = [
    path('', include_docs_urls(title='API Documentation')),
]