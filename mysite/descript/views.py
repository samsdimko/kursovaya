import random
import os
import csv
import pandas as pd
from descript.models import Question, AnswerChoice, Page, DataInput
from django.shortcuts import render
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalReadView
from .forms import *


class IndexView(generic.ListView):
    def __init__(self):
        self.page_id = 1
        self.template_name = 'descript/index.html'
        self.context_object_name = 'latest_page_list'
        df = pd.read_csv('mainfile.csv', sep='|', dtype='string', index_col=0)
        self.data = df[df['is_ready'] == str(0)].sample(n=1)['idx'].values[0]
#        self.data = str(sorted(os.listdir('/home/samsdimko/Site/mysite/descript/static'))[random.randint(0, len(os.listdir('/home/samsdimko/Site/mysite/descript/static')))])
    def get_context_data(self, **kwargs):
        context = context = super().get_context_data(**kwargs)
        context['ima'] = self.data
        context['page_id'] = self.page_id
        context['text'] = ''
        context['form'] = PageZeroForm
        return context
    def get_queryset(self):
        pass

def name(request, page_id, ima):     
    f = PageZeroForm(request.POST)
    f.is_valid()
    request.session.modified = True
    if f.cleaned_data['name'] != '':
        request.session['name'] = f.cleaned_data['name']
    else:
        request.session['name'] = 'DEFAULT_ANONIMUS_USER'
    return HttpResponseRedirect(reverse('descript:page', args=(1, 0, ima,)))
       
class ModalView(BSModalReadView):
    def __init__(self):        
        self.model = Page
        self.template_name = 'descript/mymodal.html'        
        self.data = pd.read_csv('addfile.csv', sep='|', dtype='string', header=0, names=['name','description_en','description_ru'], index_col=0)
        self.page_id = random.randint(0, len(self.data))
        self.object = 0

    class META:
        model = Page
        app_label = 'modal'
        data = pd.read_csv('addfile.csv', sep='|', dtype='string', header=0, names=['name','description_en','description_ru'], index_col=0)
        def get(self, *args):            
            return render(request, 'descript/mymodal.html', context=context)
            
    def get_context_data(self, **kwargs):
        context = context = super().get_context_data(**kwargs)
        context['ima'] = self.data['name'][self.page_id + 1]
        if pd.isnull(self.data['description_ru'][self.page_id]) == False:
            context['text'] = self.data['description_ru'][self.page_id]
        else:
            context['text'] = self.data['description_en'][self.page_id]
        return context
        
    def get(self, request, **kwargs):
        context = ModalView.get_context_data(self, **kwargs)
        return render(request, 'descript/mymodal.html', context=context)  

class Page1View(generic.DetailView):
    def __init__(self):
        self.page_id = 1
        self.model = Page
        self.template_name = 'descript/Page1.html'        
        self.data = ''
        self.object = 0

    class META:
        model = Page
        app_label = 'descript'
        def get(self, *args):            
            return render(request, 'descript/Page1.html', context=context)
            
    def get_context_data(self, **kwargs):
        context = context = super().get_context_data(**kwargs)
        text_switcher = {
                1:'',
                2:'Как вы предпочтете описывать изображение?',
                3:'Пожалуйста, опишите полностью происходящее на изображении, включая фон',
                4:'Пожалуйста, опишите самого(их) персонажа(ей). Какого он(и) пола, вида, сколько всего персонажей и прочее',
                5:'Опишите его(их) положение в кадре, что он(и) делает(ют)',
                5:'Опишите его(их) одежду',
                6:'С чем он(и) взаимодействует(ют), что держит(ют) в руках?',
                7:'Коротко опишите фон',
                8:'Пожалуйста, полностью опишите персонажа',
                9:'Пожалуйста, опишите самого персонажа. Какого он пола, вида и прочее',
                10:'Опишите положение в кадре, что персонаж делает',
                11:'Опишите его одежду',
                12:'С чем он взаимодействует, что держит в руках?',
                13:'Продолжим?',
                14:'Коротко опишите фон'
        }
        form = form_switcher(self.page_id)
        context['text'] = text_switcher[self.page_id]
        context['ima'] = self.data
        context['form'] = form
        context['page_id'] = self.page_id
        context['text'] = text_switcher[self.page_id]      
        return context
        
    def get(self, request, **kwargs):
        if int(kwargs['page_id']) == 0:
            self.page_id = 1
            df = pd.read_csv('mainfile.csv', sep='|', dtype='string', index_col=0)
            self.data = df[df['is_ready'] == str(0)].sample(n=1)['idx'].values[0]
            context = Page1View.get_context_data(self, **kwargs)
            return render(request, 'descript/Page1.html', context=context)
        else:
            self.data = kwargs['ima']
            self.page_id = int(kwargs['pk'])
            context = Page1View.get_context_data(self, **kwargs)
            return render(request, 'descript/Page1.html', context=context)


def form_switcher(number):
    return {
                number == 1: PageOneForm,
                number == 2: PageTwoForm,
                number == 3: PageMainQuestionForm,
            3 < number <= 7: PageSecondaryQuestionForm,
                number == 8: PageMainParticalQuestionForm,
            8 < number <= 12: PageSecondaryParticalQuestionForm,
                number == 13: PageContinueQuestionForm,
                number == 14: PageSecondaryParticalQuestionForm            
           }[True]

def quest(request, page_id, ima): 
    print(request.session)
    def set_value(ans_n, ans):
        df = pd.read_csv('mainfile.csv', sep='|', dtype='string', header=0, index_col=0)
        if ans_n == 'is_ready':
            df.loc[df['idx'] == ima, ans_n] = ans
        elif pd.isnull(df.loc[df['idx'] == ima, ans_n].values[0]) == True:
            df.loc[df['idx'] == ima, ans_n] = ans
        else:
            df.loc[df['idx'] == ima, ans_n] = (df.loc[df['idx'] == ima, ans_n] + ' ~ ' + ans)
        df.loc[df['idx'] == ima, 'name'] = request.session['name']        
        df.to_csv('mainfile.csv', sep='|')
    
    def get_back_value(ima):
        df = pd.read_csv('mainfile.csv', sep='|', dtype='string', header=0, index_col=0)
        if pd.isnull(df.loc[df['idx'] == ima, 'ans10_1'].values[0]) == True:
            return False
        else:
            return True
    
    def switch(results, page_id, ima):
        if page_id == 1:      
            set_value('isnull', results['ans1'])
            if int(results['ans1']) == 1:                
                set_value('is_ready', '1')
                return HttpResponseRedirect(reverse('descript:page', args=(0, 0, ima,)))
            else:
                return HttpResponseRedirect(reverse('descript:page', args=(2, 2, ima,))) 
                        
        if page_id == 2:
            if int(results['ans1']) == 0:
                if int(results['ans2']) == 0:
                    return HttpResponseRedirect(reverse('descript:page', args=(8, 8, ima,)))
                else:
                    return HttpResponseRedirect(reverse('descript:page', args=(9, 9, ima,)))                   
            else:
                if int(results['ans2']) == 0:
                     return HttpResponseRedirect(reverse('descript:page', args=(3, 3, ima,)))                 
                else:
                    return HttpResponseRedirect(reverse('descript:page', args=(4, 4, ima,)))       
            
        if page_id == 3:
            if int(results['ans2']) == 1:
                return HttpResponseRedirect(reverse('descript:page', args=(4, 4, ima,))) 
            set_value('full_ans', results['ans1'])
            if results['ans2'] != '':
                set_value('is_ready', '1')
            return HttpResponseRedirect(reverse('descript:page', args=(0, 0, ima,))) 
                
        if page_id == 4:
            if int(results['ans2']) == 1:
                return HttpResponseRedirect(reverse('descript:page', args=(3, 3, ima,))) 
            set_value('ans4', results['ans1'])
            return HttpResponseRedirect(reverse('descript:page', args=(5, 5, ima,)))  
        
        if page_id == 5:
            if int(results['ans2']) == 1:
                return HttpResponseRedirect(reverse('descript:page', args=(3, 3, ima,)))         
            set_value('ans5', results['ans1'])
            return HttpResponseRedirect(reverse('descript:page', args=(6, 6, ima,)))  

        if page_id == 6:
            if int(results['ans2']) == 1:
                return HttpResponseRedirect(reverse('descript:page', args=(3, 3, ima,)))         
            set_value('ans6', results['ans1'])
            return HttpResponseRedirect(reverse('descript:page', args=(7, 7, ima,)))  

        if page_id == 7:
            if int(results['ans2']) == 1:
                return HttpResponseRedirect(reverse('descript:page', args=(3, 3, ima,)))        
            set_value('ans7', results['ans1'])
            return HttpResponseRedirect(reverse('descript:page', args=(0, 0, ima,)))              
        
        if page_id == 8:
            if int(results['ans2']) == 1:
                return HttpResponseRedirect(reverse('descript:page', args=(9, 9, ima,)))         
            set_value('ans8', results['ans1'])
            return HttpResponseRedirect(reverse('descript:page', args=(14, 14, ima,)))     
            
        if page_id == 9:
            if int(results['ans2']) == 1:
                return HttpResponseRedirect(reverse('descript:page', args=(8, 8, ima,)))        
            set_value('ans9', results['ans1'])
            return HttpResponseRedirect(reverse('descript:page', args=(10, 10, ima,)))         
            
        if page_id == 10:
            if int(results['ans2']) == 1:
                return HttpResponseRedirect(reverse('descript:page', args=(8, 8, ima,)))           
            set_value('ans10', results['ans1'])
            return HttpResponseRedirect(reverse('descript:page', args=(11, 11, ima,)))
            
        if page_id == 11:
            if int(results['ans2']) == 1:
                return HttpResponseRedirect(reverse('descript:page', args=(8, 8, ima,)))           
            set_value('ans11', results['ans1'])
            return HttpResponseRedirect(reverse('descript:page', args=(12, 12, ima,)))        
           
        if page_id == 12:
            if int(results['ans2']) == 1:
                return HttpResponseRedirect(reverse('descript:page', args=(8, 8, ima,)))           
            set_value('ans12', results['ans1'])
            return HttpResponseRedirect(reverse('descript:page', args=(13, 13, ima,)))           
        
        if page_id == 13:
            if int(results['ans1']) == 0:
                return HttpResponseRedirect(reverse('descript:page', args=(9, 9, ima,)))
            elif int(results['ans1']) == 1:
                return HttpResponseRedirect(reverse('descript:page', args=(3, 3, ima,)))
            else:
                return HttpResponseRedirect(reverse('descript:page', args=(14, 14, ima,)))
                
        if page_id == 14:        
            set_value('ans14', results['ans1'])
            return HttpResponseRedirect(reverse('descript:page', args=(0, 0, ima,)))
             
    page_id = int(page_id)
    if request.method == 'POST':        
        form = form_switcher(page_id)        
        f = form(request.POST)
        f.is_valid()
        return switch(f.cleaned_data, page_id, ima)
    return HttpResponseRedirect('/descript/1/')


       
def next_page(request, page_id, one): 
    if int(one) == 0:
        page_id = int(page_id) - 1
    else:
        page_id = int(page_id) + 1
    num_desc = len(pd.read_csv('addfile.csv', sep='|', dtype='string'))
    if request.method == 'POST':
        if page_id > num_desc:
            return HttpResponseRedirect(reverse('descript:modal', args=(num_desc, num_desc)))
        elif page_id < 1:
            return HttpResponseRedirect(reverse('descript:modal', args=(1, 1)))
        else:
            return HttpResponseRedirect(reverse('descript:modal', args=(page_id, page_id)))
    else:
        return HttpResponseRedirect('/modal/1/')
           
"""        
form_switcher = {
                1: PageOneForm,
                2: PageTwoForm,
                3: PageMainQuestionForm,
                4: PageFourFormAntr,                
                5: PageFiveForm,
                6: PageSixForm,
                7: PageSevenForm,
                8: PageEightForm,
                9: PageNineForm,
                10: PageTenForm,
                11: PageElevenForm,
                12: PageFourFormNotAntr,
                13: PageThirteenForm
            }

"""
