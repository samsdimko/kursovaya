from django.contrib import admin
from descript.models import Question, AnswerChoice, Page

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1

class ChoiceInline(admin.StackedInline):
    model = AnswerChoice
    extra = 1
       
class QuestionAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]

class ChoiceAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    
    
admin.site.register(Page, QuestionAdmin)
admin.site.register(Question, ChoiceAdmin)
