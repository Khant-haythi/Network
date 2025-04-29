import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render,redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import User,Post,Follow



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
            return HttpResponseRedirect(reverse("all_posts"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("all_posts"))


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
        return HttpResponseRedirect(reverse("all_posts"))
    else:
        return render(request, "network/register.html")

def all_posts(request):
    post_list = Post.objects.all().order_by('-created_date')  # Get all posts, ordered by descending
    paginator = Paginator(post_list, 10)  # 10 posts per page

    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)  

    return render(request, 'network/index.html', {'posts': posts})

def create_post(request):

    if request.method == "POST": 
        
        content = request.POST.get('content')
        posting = Post(owner=request.user,content=content)
        posting.save()
        messages.success(request, "Post successfully created!")
        return redirect('all_posts')
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

def following(request):
    if request.user.is_authenticated:
        following_users = Follow.objects.filter(follower=request.user).values_list('following', flat=True)
        posts = Post.objects.filter(owner__in=following_users).order_by('-created_date')
    else:
        posts = []
    
    return render(request, 'network/following.html', {'posts': posts})

@login_required
def edit_post(request, post_id):
    
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        post = Post.objects.get(id=post_id)
        
        if post.owner != request.user:
            return JsonResponse({"error": "Unauthorized"}, status=403)

        data = json.loads(request.body)
        content = data.get("content")

        if not content:
            return JsonResponse({"error": "Content required"}, status=400)

        post.content = content
        post.save()

        return JsonResponse({
            "success": True,
            "updated_content": content
        })

    except Post.DoesNotExist:
        return JsonResponse({"error": "Not found"}, status=404)
    
@login_required
def like_post(request, post_id):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        post = Post.objects.get(id=post_id)
        
        if post.owner == request.user:
            return JsonResponse({"error": "Cannot like your own post"}, status=403)

        # Check if the user has already liked the post
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            liked = False
        else:
            post.likes.add(request.user)
            liked = True

        return JsonResponse({
            "success": True,
            "likes": post.likes.count(),
            "liked": liked
        })

    except Post.DoesNotExist:
        return JsonResponse({"error": "Not found"}, status=404)
        