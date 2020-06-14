from django.shortcuts import render
from django.views.generic import DetailView
from .forms import UserRegistrationForm
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
            
            return render(request, 'registration/register_done.html', {'user':new_user}) #rendering different page and passing user

        else:
            return render(request, 'registration/register.html', {'form':user_form})


    else:
        user_form = UserRegistrationForm()
        return render(request, 'registration/register.html', {'form':user_form})

