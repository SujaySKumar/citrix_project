from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from citrix_answers.models import Question, Answer, Tag
from django.template import context
from django.db.models import Q

import spam

import operator

# Create your views here.
def home(request):
	context = {}
	return render(request, 'homepage.html',context)

def test_view(request):
    if request.user.is_authenticated():
        all_questions = Question.objects.all().order_by('-views')
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
    answers = list(Answer.objects.filter(question=question).order_by('-upvotes'))
    accepted_answer = list(Answer.objects.filter(question=question).filter(is_solution=1))

    if len(accepted_answer) == 1:
            answers.remove(accepted_answer[0])
    accepted_answer.extend(answers)
    context = {
            'answer_list': accepted_answer,
            'question': question,
            #'accepted_answer': accepted_answer
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
        question_content = request.POST['new_question_title']
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

def search(request):
	idseq = request.POST['search_term'].split()
	tag_search = request.POST['search_term'].startswith("#")

	if(tag_search):
		tag = request.POST['search_term'].split()
		if(len(tag) > 1):
			result = Question.objects.filter(reduce(operator.or_, (Q(tags__tag_name = x[1:]) for x in tag))).order_by('updated_at')
		else:
			result = Question.objects.filter(tags__tag_name = tag[0][1:])
	else:
		result = Question.objects.filter(Q(title__icontains = idseq)|reduce(operator.or_, (Q(title__icontains = x) for x in idseq))).order_by('updated_at')

	context = {'search_question_list' : result}
	return render(request, 'search_questions_list.html', context)

def accept_solution(request):
        answer_id = int(request.GET['answer_id'][:-16])
        answer = Answer.objects.get(pk=answer_id)

        q = answer.question
        q.has_solution = 1
        q.save()

        answer.is_solution = 1
        answer.save()
        return JsonResponse({'result': 'success'})

def check_spam(request):
        text = request.GET['title_text']
        filename = 'citrix_answers/data/Data.csv'
	spam.load(filename)
	prob = spam.query(text)
        if prob > 0.5:
                return JsonResponse({'spam': 'True'})
        else:
                return JsonResponse({'spam': 'False'})
