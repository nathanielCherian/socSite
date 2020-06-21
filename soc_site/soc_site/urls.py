"""soc_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from ckeditor_uploader import views as ckviews
from users import views as user_views

urlpatterns = [
    path('users/<slug:user>', user_views.view_profile, name='view_profile'),
    path('admin/', admin.site.urls),
    path('', include('feed.urls')), #this will import all of the urls created in the feed app
    path('settings/', include('usettings.urls')), #all of the user settings
    path('account/', include('users.urls')), #this will import all of the urls created in the feed app
    path('upload/', ckviews.upload, name='ckeditor_upload'),
    path('browse/', ckviews.browse, name='ckeditor_browse'),
    path('posts/<slug:tag_slug>/', user_views.view_by_tag, name='view_by_tag'),
    path('discussions/', include('discussions.urls'))
   

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)