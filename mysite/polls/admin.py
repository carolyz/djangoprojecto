from django.contrib import admin

# Register your models here.
from .models import Choice, Question #import Question objs so it has admin interface
# admin.site.register(Question) #register Question so it's on the admin index page

class ChoiceInline(admin.TabularInline):
	model = Choice
	extra = 3 #how many slots for Choices

class QuestionAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields': ['question_text']}),
		('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
	]
	inlines = [ChoiceInline]
	list_display = ('question_text', 'pub_date', 'was_published_recently')

	#adds Filter sidebar allowing Q list to be filtered by date
	list_filter = ['pub_date']

	#can search question_text field by terms
	search_fields = ['question_text']

admin.site.register(Question, QuestionAdmin)	