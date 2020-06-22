from django.urls import path
from . import views as views

urlpatterns = [
    path('', views.QuestionListView.as_view(), name='discussion_board'),
    path('create/', views.create_question, name='create_question'),
    path('<slug:question_slug>/', views.view_question, name='view_question'),

]