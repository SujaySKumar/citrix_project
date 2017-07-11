from django.shortcuts import render
from django.http import HttpResponse
from citrix_answers.models import Question, Answer
from django.template import context

# Create your views here.
def home(request):
	context = {}
	return render(request, 'homepage.html',context)

def test_view(request):
    if request.user.is_authenticated():
        all_questions = Question.objects.all()
        context = {'question_list': all_questions}
        return render(request, 'questions_list.html', context)
    else:
        return HttpResponse("User is not logged in!")

def question_answer_view(request, question_id):
    question = Question.objects.get(pk=question_id)
    question.views = question.views+1
    question.save()
    answers = Answer.objects.filter(question=question)
    context = {
        'answer_list': answers,
        'question': question
    }
    return render(request, 'question_answer.html', context)

def add_answer(request, question_id):
    question = Question.objects.get(pk=question_id)
    answer = Answer(
        content=request.POST['new_answer'],
        question=question,
        user=request.user
    )
    answer.save()
    return HttpResponse("Answer added successfully")

def add_question(request):
    question = Question(
        title=request.POST['new_question_title'],
        description=request.POST['new_question_description'],
        user=request.user
    )
    question.save()
    return HttpResponse("Question added successfully")
