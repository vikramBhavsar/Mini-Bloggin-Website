from django.forms import ModelForm
from .models import Comment,Post
from django.contrib.auth.models import User

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["author","title","text"]

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["author","text"]

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ["first_name","last_name","email","password"]

