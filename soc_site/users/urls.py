from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('create/', views.create_post, name='create_post'),
    path('drafts/', views.saved_drafts, name='saved_drafts'),
    path('edit/<slug:post_slug>/', views.edit_post, name='edit_post'),
    path('edit/', views.edit_profile, name='edit_profile'),

    path('settings/', views.account_settings, name='profile_settings'),
    path('settings/security/', auth_views.PasswordChangeView.as_view(), name='account_security'),
    path('settings/security/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

]