
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("following/", views.following, name="following"),

    path("user_profile/<str:user_name>",
         views.user_profile, name="user_profile"),


    # API

    path("feeds", views.new_feed, name="new_feed"),
    path("feeds/<int:feedsid>", views.feeds_id, name="feeds_id"),
    path("feeds/<str:userid>", views.user_id, name="user_id"),
    path("following_feeds", views.following_feeds, name="following_feeds"),
    path("follows/<str:user_follow>", views.follow_users, name="follow_users"),




]
