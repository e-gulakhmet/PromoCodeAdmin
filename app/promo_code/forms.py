from django import forms



class NewCodeForm(forms.Form):
    amount = forms.IntegerField(label="Количество кодов")
    group = forms.CharField(label="Название группы")