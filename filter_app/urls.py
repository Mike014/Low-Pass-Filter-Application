# filter_app/urls.py

from django.urls import path
from .views import IndexView

app_name = 'filter_app'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
]
