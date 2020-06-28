from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.contrib import messages
from django.views.generic import ListView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from users.models import Notification
from .models import Question, Response
from .forms import QuestionCreateForm, ResponseCreateForm, QuestionEditForm, ResponseEditForm

class QuestionListView(ListView):
    template_name = 'discussions/board.html'
    context_object_name = 'questions'

    def get_queryset(self, **kwargs):

        print(self.request.GET)

        if self.request.GET.get('filter') == 'newest':
            return Question.actives.all().order_by('-date_posted')

        elif self.request.GET.get('filter') == 'top':
            return Question.actives.all().annotate(num_replies=Count('responses')).order_by('-num_replies')

        elif self.request.GET.get('filter') == 'random':
            return Question.actives.all().order_by('?')
        else:
            return Question.actives.all()

@login_required
def create_question(request):

    if request.method == 'POST':

        form = QuestionCreateForm(request.POST)

        if form.is_valid():
            new_question = form.save(commit=False)
            user = request.user
            new_question.author = user
            new_question.save()

            return redirect('view_question', new_question.slug)

        else:
             return render(request, 'discussions/create.html', {'form':form})

    form = QuestionCreateForm()
    return render(request, 'discussions/create.html', {'form':form})

    


def view_question(request, question_slug):
    question = get_object_or_404(Question, slug=question_slug, active=True)

    if request.method == 'POST':

        response_form = ResponseCreateForm(request.POST)

        print(request.POST)
        if response_form.is_valid():
            new_response = response_form.save(commit=False)
            new_response.author = request.user
            new_response.parent_question = question
            new_response.save()

            noti = Notification(title=f'{request.user} responded to your question "{question.title[:50]}"!', user=question.author.profile)
            noti.save()


            return redirect('view_question', question.slug)





    response_form = ResponseCreateForm(auto_id='response_%s')

    question_edit_form = None
    if question.author == request.user:
        question_edit_form = QuestionEditForm(instance=question)

    return render(request, 'discussions/view.html', {'question':question, 'response_form':response_form, 'question_edit_form':question_edit_form,})


@login_required
def edit_question(request, question_slug):
    question = get_object_or_404(Question, slug=question_slug, active=True)

    if request.method == 'POST':
    
        question_edit_form = QuestionEditForm(request.POST, instance=question)


        if question_edit_form.is_valid() and question.author == request.user:

            q = question_edit_form.save(commit=False)
            q.author = question.author
            q.save()
            return redirect('view_question', question.slug)

        
    return redirect('view_question', question.slug)


class QuestionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Question
    success_url = '/discussions'

    def get_object(self):
        return self.model.objects.get(slug=self.kwargs['question_slug'])

    def test_func(self):
        print(self.kwargs['question_slug'])
        question = self.get_object()
        if self.request.user == question.author:
            return True
        return False


@login_required
def delete_response(request, question_slug, response_pk):

    response = Response.actives.filter(pk = response_pk, parent_question__slug = question_slug).first()

    
    if response:
        if request.user == response.author:
            response.delete()
            messages.success(request, f'Response Deleted!')

    return redirect('view_question', question_slug)




@login_required
def edit_response(request, question_slug, response_pk):

    response = Response.actives.filter(pk = response_pk, parent_question__slug = question_slug).first()

    if response:
        if request.user == response.author:

            question = get_object_or_404(Question, slug=question_slug, active=True)


            if request.method == 'POST':

                respose_edit_form = ResponseEditForm(request.POST, instance=response)

                if respose_edit_form.is_valid():
                    edited_r = respose_edit_form.save(commit=False)
                    edited_r.author = request.user
                    edited_r.save()
                    messages.success(request, f'Response Updated Successfully!')
                    return redirect('view_question', question.slug)


            response_edit_form = ResponseEditForm(instance=response)

            return render(request, 'discussions/view_edit.html', {'question':question, 'response_pk':response_pk, 'response_edit_form':response_edit_form})


    return redirect('view_question', question_slug)