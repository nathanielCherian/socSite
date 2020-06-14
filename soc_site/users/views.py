from django.shortcuts import render
from django.views.generic import DetailView
from .models import Profile


class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'users/profile_detail.html'
