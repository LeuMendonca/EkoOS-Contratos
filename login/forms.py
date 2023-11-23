from django import forms
from .models import Login

class FormLogin(forms.ModelForm):
    class Meta:
        model = Login
        fields = ['login','password']
        
        widgets = {
            'login': forms.TextInput(attrs={'placeholder':'Digite seu login','name':'login', 'id':'login','autofocus':'true'}),
            'password': forms.TextInput(attrs={'placeholder':'Digite sua senha','name':'password', 'id':'password','type':'password'}),
            
        }