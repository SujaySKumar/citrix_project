from django.contrib import admin
from citrix_answers.models import Question, Answer, Employee

# Register your models here.
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Employee)
