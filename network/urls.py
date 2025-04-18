
from django.urls import path

from . import views

urlpatterns = [
    path("", views.all_posts, name="all_posts"),
    path("newpost", views.newpost, name="newpost"),
    path("login/", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createpost",views.create_post,name="create_post"),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('follow/<str:username>/', views.follow_unfollow, name='follow_unfollow'),
    path('following/', views.following, name='following'),

]
