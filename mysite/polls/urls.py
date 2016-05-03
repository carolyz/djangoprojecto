from django.conf.urls import url

from . import views

#set app namespace so django can differentiate url names for different apps
app_name = 'polls'

#call view, map to url using URLconf
urlpatterns = [
	# /polls/
	url(r'^$', views.index, name='index'),
	# /polls/5/
	url(r'^(?P<question_id>[0-9]+)/$',views.detail, name = 'detail' ), 
	# /polls/5/results
	url(r'^(?P<question_id>[0-9]+)/results/$',views.results, name = 'results' ), 
	# /polls/5/vote/
	url(r'^(?P<question_id>[0-9]+)/vote/$',views.vote, name = 'vote' ), 
	]