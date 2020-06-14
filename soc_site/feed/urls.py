from django.urls import path
from .views import PostListView, PostDetailView
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='home_feed'),
    path('<slug:slug>/', PostDetailView.as_view(), name='post_detail')
]