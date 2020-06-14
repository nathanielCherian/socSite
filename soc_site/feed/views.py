from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from .models import Post
from users.models import Profile


class PostListView(ListView):
    queryset = Post.published.all()
    template_name = 'feed/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']

'''
class PostDetailView(DetailView):
    model = Profile '''

def post_detail_view(request, author, post):
    post = get_object_or_404(Post, slug=post, author__username=author)
    return render(request, 'feed/post_detail.html', {'object':post})
    

