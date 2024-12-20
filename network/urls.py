
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("newpost", views.newpost, name="newpost"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createpost",views.create_post,name="create_post"),
    path('all_posts/', views.all_posts, name='all_posts')

]
