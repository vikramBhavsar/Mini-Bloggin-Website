from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
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

class DeletePostView(LoginRequiredMixin,DeleteView):
    model = Post
    success_url = reverse_lazy("post_list")


class DraftPostList(LoginRequiredMixin,ListView):
    login_url = "/login/"

    model = Post

    def get_queryset(self):
        return Post.objects.filter(publish_date__isnull=True).order_by("-create_date")

@login_required
def publish_post(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect("post_list")


###################################################################
###################################################################
## Below code is related to Comments ##


@login_required
def add_comment_to_post(request,pk):

    if request.method == "POST":
        post = get_object_or_404(Post,pk=pk)

        comment_info = CommentForm(request.POST)

        if comment_info.is_valid():
            comment_obj = comment_info.save(commit=False)
            comment_obj.post = post
            comment_obj.save()
            return redirect("post_detail",pk=post.pk)
    else:
        comment_form = CommentForm()

    return render(request,"blog/comment_form.html",{"comment_form":comment_form})



@login_required
def approve_comment(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    comment.approve()
    return redirect("post_detail",pk=comment.post.pk)

@login_required
def remove_comment(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect("post_detail",pk=post_pk)


###################################################################
###################################################################
## Below code is related to User Login and registration ##

