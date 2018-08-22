from django.urls import path, re_path
from .views import APIGameListCreateView, APIGameDetailUpdateView

urlpatterns = [
    path('games/', APIGameListCreateView.as_view(), name='games'),
    re_path(r'^games/(?P<pk>[0-9]+)$', APIGameDetailUpdateView.as_view(), name='detail')
]
