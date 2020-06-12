from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView,ListView,DetailView,CreateView,UpdateView
from .models import Comment,Post
from .forms import PostForm,CommentForm
from django.utils import timezone

# Create your views here.

def base(request):
    return render(request,"blog/base.html",{})


class AboutView(TemplateView):
    template_name="blog/about.html"


class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"

    def get_queryset(self):
        return Post.objects.filter(publish_date__lte=timezone.now()).order_by("-publish_date")

class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"

class CreatePostView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    template_name = "blog/about.html"

    form_class = PostForm
    model = Post

class UpdatePostview(LoginRequiredMixin,UpdateView):
    model = Post
    form_class = PostForm