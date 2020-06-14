from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse_lazy
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView
from .models import Comment,Post
from .forms import PostForm,CommentForm,UserForm
from django.utils import timezone
from django.contrib.auth.models import User


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post"] = context["object"]
        return context
    
class CreatePostView(LoginRequiredMixin,CreateView):
    login_url = reverse_lazy("login_user")
    template_name = "blog/create_post.html"

    form_class = PostForm
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post_create_form"] = context["form"]
        return context

    def form_valid(self, form):
        form.instance.author = User.objects.get(username=self.request.user.username) 

        if "publish_post" in self.request.POST:
            form.instance.publish()
            self.success_url = reverse_lazy("post_list")
        elif "draft_post" in self.request.POST:
            self.success_url = reverse_lazy("draft_list")

        return super().form_valid(form)

class UpdatePostview(LoginRequiredMixin,UpdateView):
    model = Post
    form_class = PostForm

    template_name = "blog/update_post.html"

    
    def form_valid(self, form):
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post_form"] = context["form"]
        return context
    
class DeletePostView(LoginRequiredMixin,DeleteView):
    model = Post
    template_name = "blog/delete_post.html"
    success_url = reverse_lazy("post_list")

class DraftPostList(LoginRequiredMixin,ListView):
    login_url = "/login/"

    model = Post

    template_name = "blog/draft_list.html"

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
            comment_obj.author = User.objects.get(username=request.user.username)
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

class CreateUserView(CreateView):
    model = User
    form_class = UserForm
    template_name = "registration/registration.html"
    success_url = reverse_lazy("login_user")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_form"] = context["form"]
        return context

    def form_valid(self, form):
        form.instance.username = form.instance.email
        form.instance.set_password(form.instance.password)
        return super().form_valid(form)


def login_user(request):

    if request.method == "POST":
        username = request.POST["username_inp"]
        password = request.POST["password_inp"]

        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect("post_list")
        else:
            return redirect("login_user")
    
    else:
        return render(request,"registration/login.html",{})

@login_required
def logout_user(request):
    logout(request)
    return redirect("post_list")