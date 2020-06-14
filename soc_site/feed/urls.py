from django.urls import path
from .views import PostListView #PostDetailView
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='home_feed'),
    path('<slug:author>/<slug:post>', views.post_detail_view, name='post_detail'),
   # path('<slug:slug>/', PostDetailView.as_view(), name='post_detail')
]