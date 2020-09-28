from django.contrib.auth import authenticate, login, logout
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

import urllib.parse as urlparse
from urllib.parse import parse_qs
from urllib.request import urlopen

from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, Posts, Follow



@csrf_exempt
def index(request):

    if request.method == "POST":

        text = request.POST["new_post"]
        user = Posts(user=request.user, post_text=text, no_of_likes=0)
        user.save()

        posts = Posts.objects.all()
        posts = posts.order_by("-timestamp").all()
        page = Paginator(posts, 5)

        page_no = request.GET.get("page")
        posts = page.get_page(page_no)

        context = {"posts": posts, "page_no": page_no}
        return render(request, "network/index.html", context)

    else:

        posts = Posts.objects.all()
        posts = posts.order_by("-timestamp").all()
        page = Paginator(posts, 5)

        page_no = request.GET.get("page")
        posts = page.get_page(page_no)

        context = {"posts": posts, "page_no": page_no}
        return render(request, "network/index.html", context)


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
    return HttpResponseRedirect(reverse("login"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        if username == "":
            return render(request, "network/register.html", {
                "message": "Enter Username/Email"
            })

        if email == "":
            return render(request, "network/register.html", {
                "message": "Enter Username/Email"
            })

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

            follow = Follow(user=user, no_of_followers=0, no_of_followings=0)
            follow.save()

        except IntegrityError:
            return render(request, "network/register.html", {"message": "Username already taken."})
        login(request, user)
        return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "network/register.html")


@csrf_exempt
def new_feed(request):

    datas = Posts.objects.all()
    datas = datas.order_by("-timestamp").all()

    return JsonResponse([data.serialize() for data in datas], safe=False)

  
    

@csrf_exempt
def user_profile(request, user_name):
    template = "network/user_profile.html"
    user_names = User.objects.get(username=user_name)

    username = user_name

    posts = Posts.objects.filter(user=user_names)
    posts = posts.order_by("-timestamp").all()

    profile_id = username[0]
    diff_user = request.user.username

    page = Paginator(posts, 5)
    page_no = request.GET.get("page")
    posts = page.get_page(page_no)

    context = {"posts": posts, "profile_id": profile_id,
               "diff_user": diff_user != username, "username": username, "page_no": page_no}

    return render(request, template, context)


@csrf_exempt
def user_id(request, userid):

    user_names = User.objects.get(username=userid)

    posts = Posts.objects.filter(user=user_names)
    posts = posts.order_by("-timestamp").all()

    return JsonResponse([data.serialize() for data in posts], safe=False)


@csrf_exempt
def feeds_id(request, feedsid):

    try:
        data = Posts.objects.get(pk=feedsid)
    except data.DoesNotExist:
        return JsonResponse({"error": "Not found."}, status=404)

    if request.method == "GET":
        return JsonResponse(data.serialize())

    elif request.method == "PUT":
        edit_data = json.loads(request.body)

        if edit_data.get("no_of_likes") is not None:

            if request.user in data.likes.all():
                data.likes.remove(request.user)
                data.no_of_likes = edit_data["no_of_likes"] - 2
                data.save()

            else:
                data.likes.add(request.user)
                data.no_of_likes = edit_data["no_of_likes"]
                data.save()

        if edit_data.get("text") is not None:
            data.post_text = edit_data["text"]

        data.save()
        return HttpResponse(status=204)

    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)


@csrf_exempt
def follow_users(request, user_follow):

    user = Follow.objects.get(user=request.user)
    user_follows = User.objects.get(username=user_follow)
    follower_user = Follow.objects.get(user=user_follows)

    if request.method == "GET":
        return JsonResponse(follower_user.serialize1())

    elif request.method == "PUT":
        follow_data = json.loads(request.body)

        if user_follows in user.followings.all():
            user.followings.remove(user_follows)
            user.no_of_followings = user.no_of_followings - 1
            user.save()

            follower_user.followers.remove(request.user)
            follower_user.no_of_followers = follow_data["no_of_followers"] - 2
            follower_user.save()

        else:
            user.followings.add(user_follows)
            user.no_of_followings = user.no_of_followings + 1
            user.save()

            follower_user.followers.add(request.user)
            follower_user.no_of_followers = follow_data["no_of_followers"]
            follower_user.save()
        return HttpResponse(status=204)


@csrf_exempt
def following(request):
    template = "network/following.html"
    login_user = request.user

    user_followings = Follow.objects.get(user=login_user)
    followings_list = user_followings.followings.all()

    feeds_list = []
    for users in followings_list:
        user_posts = Posts.objects.filter(user=users)
        for post in user_posts:
            feeds_list.append(post)
    
    page = Paginator(feeds_list, 5)
    page_no = request.GET.get("page")
    posts = page.get_page(page_no)
    

    context = {"posts": posts, "page_no": page_no}
    return render(request, template, context)


@csrf_exempt
def following_feeds(request):

    login_user = request.user

    user_followings = Follow.objects.get(user=login_user)
    followings_list = user_followings.followings.all()

    feeds_list = []
    for users in followings_list:
        user_posts = Posts.objects.filter(user=users)
        for post in user_posts:
            feeds_list.append(post)

    return JsonResponse([feeds.serialize() for feeds in feeds_list], safe=False)


