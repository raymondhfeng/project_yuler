from django import forms
from django.forms import ModelForm
from .models import MyModel

class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)

class MyModelForm(ModelForm):
    class Meta:
        model = MyModel
        fields = ['color']