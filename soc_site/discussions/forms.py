from django import forms
from .models import Question, Response

class QuestionCreateForm(forms.ModelForm):

    class Meta:
        model = Question
        fields=('title', 'content')

    def clean(self):
        title = self.cleaned_data.get('title')
        if Question.objects.filter(title=title).exists():
            raise forms.ValidationError("A question with this title already exists!")
        return self.cleaned_data


class ResponseCreateForm(forms.ModelForm):

    class Meta:
        model = Response
        fields=('content',)


class QuestionEditForm(forms.ModelForm):

    class Meta:
        model = Question
        fields=('title', 'content')

    def clean(self):
        title = self.cleaned_data.get('title')
        if len(Question.objects.filter(title=title)) > 1:
            raise forms.ValidationError("A question with this title already exists!")
        return self.cleaned_data