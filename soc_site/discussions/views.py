from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Question
from .forms import QuestionCreateForm, ResponseCreateForm

class QuestionListView(ListView):
    queryset = Question.objects.all()
    template_name = 'discussions/board.html'
    context_object_name = 'questions'


def create_question(request):

    if request.method == 'POST':

        form = QuestionCreateForm(request.POST)

        if form.is_valid():
            new_question = form.save(commit=False)
            user = request.user
            new_question.author = user
            new_question.save()

            return redirect('discussion_board')

        else:
             return render(request, 'discussions/create.html', {'form':form})

    form = QuestionCreateForm()
    return render(request, 'discussions/create.html', {'form':form})


def view_question(request, question_slug):
    question = get_object_or_404(Question, slug=question_slug)

    if request.method == 'POST':

        response_form = ResponseCreateForm(request.POST)

        if response_form.is_valid():
            new_response = response_form.save(commit=False)
            new_response.author = request.user
            new_response.parent_question = question
            new_response.save()
            return redirect('view_question', question.slug)


    response_form = ResponseCreateForm()
    return render(request, 'discussions/view.html', {'question':question, 'response_form':response_form,})
