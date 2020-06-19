from django import forms
from django.contrib.auth.models import User
from feed.models import Post
from .models import Profile

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Reapeat Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("Passwords dont match")
        return cd['password2']

    def clean(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already in Use!")
        
        return self.cleaned_data

class PostCreateForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'summary', 'content', 'tags', 'status')


