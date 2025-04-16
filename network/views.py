from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render,redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import User,Post,Follow


def index(request):
    posts = Post.objects.all()
    return render(request, "network/index.html",{'posts': posts})

def newpost(request):
    return render(request,"network/post.html")


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def all_posts(request):
    posts = Post.objects.all().order_by('created_date')  # Get all posts, ordered by most recent
    return render(request, 'network/index.html', {'posts': posts})

def create_post(request):

    if request.method == "POST": 
        
        content = request.POST.get('content')
        posting = Post(owner=request.user,content=content)
        posting.save()
        messages.success(request, "Post successfully created!")
        return redirect('index')
    return render(request, 'network/post.html')  

def profile(request, username):
    user = User.objects.get(username=username)
    posts = Post.objects.filter(owner=user).order_by('-created_date')
    followers_count = Follow.objects.filter(following=user).count()
    following_count = Follow.objects.filter(follower=user).count()
    
    is_following = Follow.objects.filter(follower=request.user, following=user).exists() if request.user.is_authenticated else False

    return render(request, 'network/profile.html', {
        'user': user,
        'posts': posts,
        'followers_count': followers_count,
        'following_count': following_count,
        'is_following': is_following
    })

@login_required
def follow_unfollow(request, username):
    if request.method == "POST":
        profile_user = get_object_or_404(User, username=username)
        
        # Check if already following
        follow_obj = Follow.objects.filter(follower=request.user, following=profile_user).first()
        
        if follow_obj:
            # Unfollow
            follow_obj.delete()
            is_following = False
           
        else:
            # Follow
            Follow.objects.create(follower=request.user, following=profile_user)
            is_following = True
            
        
        # Update follower count
        follower_count = Follow.objects.filter(following=profile_user).count()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'is_following': is_following,
                'follower_count': follower_count
            })
        return redirect('profile', username=username)
    return redirect('profile', username=username)

def following (request):
    if request.user.is_authenticated:
        following_users = Follow.objects.filter(follower=request.user).values_list('following', flat=True)
        posts = Post.objects.filter(owner__in=following_users).order_by('-created_date')
    else:
        posts = []
    
    return render(request, 'network/following.html', {'posts': posts})