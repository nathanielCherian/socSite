from django.urls import path
from . import views as views

urlpatterns = [
    path('', views.discussion_board, name='discussion_board'),
]