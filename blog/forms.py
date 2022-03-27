from django import forms
from django.forms import ModelForm
from .models import BlogPost

class LoginForm(forms.Form):
    username = forms.CharField(label='username', max_length=100)
    password = forms.PasswordInput()

class PostCreationForm(ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'is_published']
