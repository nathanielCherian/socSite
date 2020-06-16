from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import slugify
from feed.models import Post
from .forms import UserRegistrationForm, PostCreateForm
from .models import Profile


class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'users/profile_detail.html'


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)

        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password']) #using .set_password to invoke hashing algorithm
            new_user.save()
            
            profile = Profile.objects.create(user=new_user)
            profile.slug = slugify(new_user.username)
            profile.save()

            return render(request, 'registration/register_done.html', {'user':new_user}) #rendering different page and passing user

        else:
            return render(request, 'registration/register.html', {'form':user_form})


    else:
        user_form = UserRegistrationForm()
        return render(request, 'registration/register.html', {'form':user_form})


@login_required
def view_profile(request, user):
    profile = get_object_or_404(Profile, slug=user)
    posts = Post.published.filter(author=profile.user).order_by('-date_posted')
    return render(request, 'account/view_profile.html', {'profile':profile, 'posts':posts})


@login_required
def create_post(request):

    
    if request.method == 'POST':
        post_form = PostCreateForm(request.POST)

        if post_form.is_valid():



            user = request.user
            new_post = post_form.save(commit=False)
            new_post.author = user
            new_post.save()

            if post_form.cleaned_data.get('status')== 'draft':
                return redirect('view_profile', user)
    
            return redirect('home_feed')

        else:
            return render(request, 'account/create_post.html', {'form':post_form})

    else:
        form = PostCreateForm()
        return render(request, 'account/create_post.html', {'form':form})



@login_required
def saved_drafts(request):
    drafts = Post.objects.filter(author=request.user, status='draft').order_by('-date_posted')
    return render(request, 'account/saved_drafts.html', {'posts':drafts})