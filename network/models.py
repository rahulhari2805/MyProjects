from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Posts(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_post")
    post_text = models.TextField(blank=True)
    likes = models.ManyToManyField(User)
    no_of_likes = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return{
            "id": self.id,
            "user_name": self.user.username,
            "text": self.post_text,
            "likes": [user.username for user in self.likes.all()],
            "no_of_likes": self.no_of_likes,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p")
        }


class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="follow_user")

    followers = models.ManyToManyField(User, related_name="followers_of_user")
    no_of_followers = models.IntegerField()

    followings = models.ManyToManyField(
        User, related_name="followings_of_user")
    no_of_followings = models.IntegerField()

    def serialize1(self):
        return {
            "user": self.user.username,
            "followers": [user.username for user in self.followers.all()],
            "no_of_followers": self.no_of_followers,
            "followings": [user.username for user in self.followings.all()],
            "no_of_followings": self.no_of_followings

        }
