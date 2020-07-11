from django.urls import path
from . import views as views

urlpatterns = [
    path('', views.QuestionListView.as_view(), name='discussion_board'),
    path('create/', views.create_question, name='create_question'),
    path('<slug:question_slug>/', views.view_question, name='view_question'),
    path('<slug:question_slug>/delete-response/<int:response_pk>/', views.delete_response, name='delete_reponse'),
    path('<slug:question_slug>/edit-response/<int:response_pk>/', views.edit_response, name='edit_response'),
    path('<slug:question_slug>/edit/', views.edit_question, name='edit_question'),
    path('<slug:question_slug>/delete/', views.QuestionDeleteView.as_view(), name='delete_question'),
    path('<slug:question_slug>/upvote/', views.upvote, name='upvote'),
    path('<slug:question_slug>/downvote/', views.downvote, name='upvote'),

]