from django.db import models
from django import forms
from abc import ABC, abstractmethod


class Page(models.Model):
    name = models.CharField(max_length=200, default='')
    def __str__(self):        
        return self.name

class Question(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200, default='')
    def __str__(self):        
        return self.question_text


class AnswerChoice(models.Model):   
    question = models.ForeignKey(Question, on_delete=models.CASCADE) 	
#    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200, default='')
    def __str__(self):        
        return self.choice_text
        
class TextAnswer(models.Model):
    text = models.CharField(max_length=200, default='')
    def __str__(self):        
        return self.text
        
        
        
class DataInput(forms.Form):
       file = forms.FileField()
       def save(self):
           records = csv.reader(self.cleaned_data["file"])
           for line in records:
               input_data = Data()
               input_data.save()
