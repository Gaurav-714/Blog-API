from django.urls import path
from .views import *

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('blog', CreateBlog.as_view()),
    path('blogs/<int:pk>', ViewUserBlogs.as_view()),
]
