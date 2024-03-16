from django import forms
from .models import Login



class LoginForm(forms.ModelForm):

    class Meta:
        model = Login
        fields = ['username', 'password']
        