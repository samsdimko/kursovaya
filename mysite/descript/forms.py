from django import forms

class PageZeroForm(forms.Form):
    name = forms.CharField(label='Введите имя для сохранения Вас в базе данных (можно оставить пустым)', required=False)

class PageOneForm(forms.Form):
    choices = ((0,'Да'),(1,'Нет'))
    ans1 = forms.ChoiceField(label='Есть ли на картинке персонажи?', choices=choices)

class PageTwoForm(forms.Form):
    choices = ((0,'Да'),(1,'Нет'))
    ans1 = forms.ChoiceField(label='Нужно ли описывать несколько персонажей по отдельности?', choices=choices, initial='1')
    choices = ((0,'Целиком'),(1,'По частям'))
    ans2 = forms.ChoiceField(label='Опишете целиком или по отдельным вопросам?', choices=choices)
    
class PageMainQuestionForm(forms.Form):
    ans1 = forms.CharField(label='', required=False, widget=forms.Textarea)
    choices = ((0, 'Описать полностью'),(1, 'Описать по частям'))
    ans2 = forms.ChoiceField(label='', choices=choices, widget=forms.RadioSelect, initial='0')

class PageSecondaryQuestionForm(forms.Form):
    ans1 = forms.CharField(label='', required=False, widget=forms.Textarea)
    choices = ((0, 'Продолжить описание по частям'),(1, 'Описать полностью'))
    ans2 = forms.ChoiceField(label='', choices=choices, widget=forms.RadioSelect, initial='0')
    
class PageMainParticalQuestionForm(forms.Form):
    ans1 = forms.CharField(label='', required=False, widget=forms.Textarea)
    choices = ((0, 'Описать полностью'),(1, 'Описать по частям'))
    ans2 = forms.ChoiceField(label='', choices=choices, widget=forms.RadioSelect, initial='0')

class PageSecondaryParticalQuestionForm(forms.Form):
    ans1 = forms.CharField(label='', required=False, widget=forms.Textarea)
    choices = ((0, 'Продолжить описание по частям'),(1, 'Описать полностью'))
    ans2 = forms.ChoiceField(label='', choices=choices, widget=forms.RadioSelect, initial='0')
    
class PageContinueQuestionForm(forms.Form):
    choices = ((0, 'Да, продолжить описание отдельных персонажей'),(1, 'Да, продолжить описание целиком'),(2, 'Нет'))
    ans1 = forms.ChoiceField(label='Продолжать описание?', choices=choices)
