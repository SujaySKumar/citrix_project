from django.conf.urls import url
from django.template import Context

from . import views

urlpatterns = [
	url(r'^homepage', views.home, name='home'),
    url(r'^test', views.test_view, name='test_view'),
    url(r'^question/(?P<question_id>[0-9]+)/$', views.question_answer_view, name='question_answer_view'),
    url(r'^add-answer/(?P<question_id>[0-9]+)/$', views.add_answer, name='add_answer'),
    url(r'^add-question/$', views.add_question, name='add_question'),
]
