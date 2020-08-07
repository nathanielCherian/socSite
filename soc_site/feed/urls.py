from django.urls import path
from .views import PostListView #PostDetailView
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='home_feed'),
    path('search/', views.get_post_queryset, name='search_posts'),    
    path('<slug:author>/<slug:post>', views.post_detail_view, name='post_detail'),
    path('<slug:author>/<slug:post>/json', views.post_detail_serialized, name='post_serialized'),

   # path('<slug:slug>/', PostDetailView.as_view(), name='post_detail')
]