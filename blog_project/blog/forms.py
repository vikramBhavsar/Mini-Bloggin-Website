from django.forms import ModelForm
from django import forms
from .models import Comment,Post
from django.contrib.auth.models import User

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["title","text"]

        widgets = {
            # "author": forms.TextInput(attrs={"class":"form-control"}),
            "title": forms.TextInput(attrs={"class":"form-control"}),
            "text": forms.Textarea(attrs={"class":"form-control","rows":2}),
        }

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["author","text"]

        widgets = {
            "author": forms.TextInput(attrs={"class":"form-control"}),
            "title": forms.TextInput(attrs={"class":"form-control"}),
        }

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ["first_name","last_name","email","password"]

        widgets = {
            "first_name": forms.TextInput(attrs={"class":"form-control"}),
            "last_name": forms.TextInput(attrs={"class":"form-control"}),
            "email": forms.EmailInput(attrs={"class":"form-control"}),
            "password": forms.PasswordInput(attrs={"class":"form-control"}),
        }

