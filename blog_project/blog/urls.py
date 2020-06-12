from django.urls import path

from . import views

urlpatterns = [
    path('posts/',views.PostListView.as_view(),name="post_list"),
    path("post/<int:pk>/",views.PostDetailView.as_view(),name="post_detail"),
    path("post/new/",views.CreatePostView.as_view(),name="create_post"),
    path("post/<int:pk>/edit/",views.UpdatePostview.as_view(),name="update_post"),
    path('about/',views.AboutView.as_view(),name="about_page"),
    path('',views.base,name='base_page'),

]
