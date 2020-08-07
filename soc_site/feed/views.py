from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from django.db.models import Q, Count
from django.core.serializers.json import DjangoJSONEncoder
from .models import Post
from discussions.models import Question
from users.models import Profile
import json


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


def post_detail_serialized(request, author, post):
    post = get_object_or_404(Post, slug=post, author__username=author, status='published')

    d = post.__dict__
    d['author_username'] = post.author.username
    d['author_firstname'] = post.author.first_name
    d['author_lastname'] = post.author.last_name

    del d['_state']

    return HttpResponse(json.dumps(d, cls=DjangoJSONEncoder), content_type="application/json")    



def get_post_queryset(request, query=None):



    filter_query = ''
    if 'filter' in request.GET:
        filter_query = request.GET['filter']
        


    if 'search' in request.GET:

        search_term = request.GET['search']

        if request.GET.get('medium') == 'Questions':
            questions = Question.actives.all()
            questions = questions.filter(Q(title__icontains=search_term) | Q(content__icontains=search_term))

            if filter_query == 'top':
                questions = questions.annotate(num_replies=Count('responses')).order_by('-num_replies')
            
            elif filter_query == 'old':
                questions = questions.order_by('-date_posted')

            else:
                questions = questions.order_by('date_posted')
        
            return render(request, 'query/query_questions.html', {'questions':questions, 'search_term':search_term, 'medium':'Questions', 'filter':filter_query})



        #if request.GET.get('filter') == 'Posts': this will be the default
    
        posts = Post.published.filter(Q(title__icontains=search_term) | Q(summary__icontains=search_term))
    
        if filter_query == 'old':
            posts = posts.order_by('-date_posted')

        else:
            posts = posts.order_by('date_posted')

        return render(request, 'query/query_posts.html', {'posts':posts, 'search_term':search_term, 'medium':'Posts', 'filter':filter_query})

