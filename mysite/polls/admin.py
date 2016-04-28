from django.contrib import admin

# Register your models here.
from .models import Question #import Question objs so it has admin interface
admin.site.register(Question) #register Question so it's on the admin index page
