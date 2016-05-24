import datetime

from django.utils import timezone
from django.test import TestCase
from django.core.urlresolvers import reverse

from .models import Question

# Create your tests here.

class QuestionMethodTests(TestCase):
	"""was_pushlished_recently() needs to return False for questions published in the future"""
	def test_was_published_recently_with_future_question(self):
		time = timezone.now() + datetime.timedelta(days=30)

		# create Question instance with future pub date
		future_question = Question(pub_date=time)

		# output needs to be FALSE
		self.assertEqual(future_question.was_published_recently(), False)

	def test_was_published_recently_with_old_question(self):
		"""was_published_recently() needs to return False for questions published more than a day ago"""
		time = timezone.now() - datetime.timedelta(days=30)
		old_question = Question(pub_date=time) #old question is one published 1-30 days ago
		self.assertEqual(old_question.was_published_recently(), False) #should return False for was_published_recently

	def test_was_published_recently_with_recent_question(self):
		"""was_published_recently() needs to return True for questions published w/in the ast day"""
		time = timezone.now() - datetime.timedelta(hours=1)
		recent_question = Question(pub_date = time)
		self.assertEqual(recent_question.was_published_recently(), True)

	def create_question(question_text, days):
		"""shortcut function to create questions given 'question_text' and given # of days offset to now """
		time = timezone.now() + datetime.timedelta(days=days)
		return Question.objects.create(question_text = question_text, pub_date = time)

class QuestionViewTests(TestCase):
	"""if no questions, display 'no polls available' """
	def test_index_view_with_no_questions(self):
		response = self.client.get(reverse('polls:index'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "No polls available")

	self.assertQuerysetEqual(response.context['latest_question_list'], [])

	def test_index_view_with_a_past_question(self):
		"""Questions with pub_date in past should be on index page; i.e. published questions should be displayed on the page"""
		#make a question
		create_question(question_text="Past question.", days=-30)
		#set proper response
		response = self.client.get(reverse('polls:index'))
		#check actual response
		self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past question.>']
			)

	def test_index_view_with_a_future_question(self):
		"""Questions published in the future should not be displayed"""
		create_question(question_test="Future question.", days=30)
		response = self.client.get(reverse('polls:index'))
		self.assertContains(response, "No polls available", status_code = 200)

	self.assertQuerysetEqual(response.context['latest_question_list'], [])

	def test_index_view_with_future_question_and_past_question(self):
		"""if both future and past questions exist, only display past questions"""
		create_question(question_text="past question", days=-30)
		create_question(question_text="future question", days=30)
		response.self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past question.>']
		)

	def test_index_view_with_past_questions(self):
		"""questions index page can display many questions"""
		create_question(question_text="past Q1", days=-30)
		create_question(question_text="past Q2", days=-5)
		response = self.clinet.get(reverse('polls:index'))
		self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: past Q2.>', '<Question: past Q1>'])

class QuestionIndexDetailTests(TestCase):
	"""detail view of Q with future pub date should return 404"""
	def test_detail_view_with_a_future_question(self):
		future_question = create_question(question_text='Future question', days = 5)
		response = self.client.get(reverse('polls:detail', args = (future_question.id,)))
		self.assertEqual(response.status_code, 404)

	def test_detail_view_with_a_past_question(self):
		"""detail view of Q already published should display question text"""
		past_question = create_question(question_text='Past Question', days = -5)
		response = self.client.get(reverse('polls:detail', args = (past_question.id,)))
		self.assertContains(response, past_question.question_text,status_code=200)
		