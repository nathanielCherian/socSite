from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import ProfileEditForm, UserEditForm
from django.contrib import messages


@login_required
def profile_settings(request):

    if request.method =='POST':
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES,)
        user_form = UserEditForm(instance=request.user, data=request.POST, user=request.user)

        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            messages.success(request, f'Profile Updated!')

        else:
            return render(request, 'usettings/profile.html', {'profile_form':profile_form, 'user_form':user_form})

    else:
        profile_form = ProfileEditForm(instance=request.user.profile)
        user_form = UserEditForm(instance=request.user)

    return render(request, 'usettings/profile.html', {'profile_form':profile_form, 'user_form':user_form})


@login_required
def edit_profile(request):
    
    if request.method == 'POST':
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)

        if profile_form.is_valid():
            profile_form.save()
    
    else:
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(request, 'account/edit_profile.html', {'profile_form':profile_form, 'profile': request.user.profile})