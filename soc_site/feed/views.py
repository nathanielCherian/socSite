from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Post
from discussions.models import Question
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
    if request.user.is_authenticated: # if statement is to protect saved drafts
        post = get_object_or_404(Post, slug=post, author__username=author)
        return render(request, 'feed/post_detail.html', {'post':post})
    else:
        post = get_object_or_404(Post, slug=post, author__username=author, status='published')
        return render(request, 'feed/post_detail.html', {'post':post})
    

def get_post_queryset(request, query=None):

    questions = Question.actives.all()

    if 'search' in request.GET:

        search_term = request.GET['search']

        if request.GET.get('filter') == 'Questions':
            questions = questions.filter(Q(title__icontains=search_term) | Q(content__icontains=search_term))
            print(questions)
            return render(request, 'feed/query_questions.html', {'questions':questions, 'search_term':search_term})

        #if request.GET.get('filter') == 'Posts': this will be the default

        posts = Post.published.filter(Q(title__icontains=search_term) | Q(summary__icontains=search_term))
        return render(request, 'feed/query_posts.html', {'posts':posts, 'search_term':search_term})

        return render(request, 'feed/query_posts.html', {'posts':posts, 'questions':questions, 'search_term':search_term})
