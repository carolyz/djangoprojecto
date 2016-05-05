from django.shortcuts import get_object_or_404, render

# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from .models import Choice, Question

def index(request):
	latest_question_list = Question.objects.order_by('-pub_date')[:5]
	context = {'latest_question_list': latest_question_list,}

	return render(request,'polls/index.html',context)

def detail(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	return render(request,'polls/detail.html',{'question':question})

def results(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = question.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		#check for key error
		#show question voting page again with error msg
		return render(request,'polls/detail.html', {
			'question': question,
			'error_message': "Y u no select choice"
			})
	else:
		selected_choice.votes += 1
		selected_choice.save()

		#ALWAYS return HttpResponseRedirect after succesfully dealing
		#when posting data, this prevents data being posted 2x if user hits BACK
	return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
