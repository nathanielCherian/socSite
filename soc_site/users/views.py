from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import slugify
from feed.models import Post
from taggit.models import Tag
from .forms import UserRegistrationForm, PostCreateForm, ProfileEditForm
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

@login_required
def edit_post(request, post_slug):

    post = get_object_or_404(Post, slug=post_slug)


    if request.method == 'POST':
        #post_form = PostCreateForm(request.POST)


        edited_post = PostCreateForm(request.POST, instance=post)
        edited_post.save()

        #if edited_post.cleaned_data.get('status') == 'draft':
        #   return redirect('view_profile', request.user.username)

        return redirect('post_detail', post.author.profile.slug, post.slug)


    else:
        post_form = PostCreateForm(instance=post)
        return render(request, 'account/edit_post.html', {'form':post_form})


@login_required
def edit_profile(request):
    
    if request.method == 'POST':
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)

        if profile_form.is_valid():
            profile_form.save()
    
    else:
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(request, 'account/edit_profile.html', {'profile_form':profile_form, 'profile': request.user.profile})


@login_required
def profile_settings(request):

    return render(request, 'account/settings.html')



def view_by_tag(request, tag_slug):
    posts = Post.published.all()
    tag = Tag.objects.filter(slug=tag_slug).first()
    #tag = get_object_or_404(Tag, slug=tag_slug)
    object_list = posts.filter(tags__in=[tag])
    return render(request, 'feed/posts_by_tag.html', {'posts':object_list, 'c_tag':tag})




