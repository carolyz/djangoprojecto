from django.conf.urls import url

from . import views

#call view, map to url using URLconf
urlpatterns = [
	url(r'^$', views.index, name='index'),
	]