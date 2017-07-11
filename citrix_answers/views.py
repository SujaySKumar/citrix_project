from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from citrix_answers.models import Question, Answer, Tag
from django.template import context

# Create your views here.
def home(request):
	context = {}
	return render(request, 'homepage.html',context)

def test_view(request):
    if request.user.is_authenticated():
        all_questions = Question.objects.all()
        all_tags = Tag.objects.all()
        context = {
                'question_list': all_questions,
                'tag_list': all_tags
        }
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
    question_tags = request.POST.getlist('question_tags')
    for tag in question_tags:
        tag_object = Tag.objects.get(tag_name=tag)
        question.tags.add(tag_object)
    return HttpResponse("Question added successfully")

def upvote(request):
        #import ipdb; ipdb.set_trace()
        answer_id = int(request.GET['answer_id'][:-8])
        answer = Answer.objects.get(pk=answer_id)
        answer.upvotes = answer.upvotes+1
        answer.save()
        return JsonResponse({'upvotes': answer.upvotes})

def downvote(request):
        #import ipdb; ipdb.set_trace()
        answer_id = int(request.GET['answer_id'][:-10])
        answer = Answer.objects.get(pk=answer_id)
        answer.downvotes = answer.downvotes+1
        answer.save()
        return JsonResponse({'downvotes': answer.downvotes})
