from django import forms
from django.contrib.auth.models import User
from feed.models import Post
from users.models import Profile


class ProfileEditForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ('photo', 'bio', 'establishment', 'social_link')


class UserEditForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
         self.user = kwargs.pop('user',None)
         super(UserEditForm, self).__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get('email')
        if self.user not in User.objects.filter(email=email) and len(User.objects.filter(email=email)) >= 1:
            raise forms.ValidationError("Email already in Use!")
        
        return self.cleaned_data