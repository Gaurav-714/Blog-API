from django.urls import path
from .views import *

urlpatterns = [
    path('user/register', RegisterView.as_view()),
    path('user/login', LoginView.as_view()),
    path('blog/<int:pk>', ViewUserBlogs.as_view()),
    path('blog/create', CreateBlog.as_view()),
    path('blog/update', UpdateBlog.as_view()),
    path('blog/delete', DeleteBlog.as_view()),
]
