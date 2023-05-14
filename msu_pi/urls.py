from django.urls import path
from . import views
from django.urls import re_path

urlpatterns = [
    re_path(r'^recommend_pis/$', views.recommend_pis, name='recommend_pis'),
    re_path(r'^uploads/$', views.upload_csv, name='upload_csv'),
    path("", views.index),
]

