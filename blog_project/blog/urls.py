from django.urls import path

from . import views

urlpatterns = [

    ### Post Model URL Patterns ###
    # CBV #
    path('posts/',views.PostListView.as_view(),name="post_list"),
    path("drafts/",views.DraftPostList.as_view(),name="draft_list"),
    path("post/<int:pk>/",views.PostDetailView.as_view(),name="post_detail"),
    path("post/new/",views.CreatePostView.as_view(),name="create_post"),
    path("post/<int:pk>/remove/",views.DeletePostView.as_view(),name="delete_post"),
    path("post/<int:pk>/edit/",views.UpdatePostview.as_view(),name="update_post"),

    # FBV #
    path("post/<int:pk>/publish/",views.publish_post,name="publish_post"),

    # Comment Model URL Patterns
    # CBV #

    # FBV #
    path('post/<int:pk>/comment/',views.add_comment_to_post,name="add_comment_to_post"),
    path('comment/<int:pk>/approve/',views.approve_comment,name="approve_comment"),
    path("comment/<int:pk>/remove",views.remove_comment,name="remove_comment"),

    ### User Model URL Patterns ###
    # CBV #
    path("register/",views.CreateUserView.as_view(),name="create_user"),

    # FBV #
    path("login/",views.login_user,name="login_user"),
    path("logout/",views.logout_user,name="logout_user"),

    # Others
    path('about/',views.AboutView.as_view(),name="about_page"),
    path('',views.base,name='base_page'),
]
