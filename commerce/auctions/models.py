from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_category")
    category = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.category}({self.user})"

class Auction_Listing(models.Model):
    Auction_user = models.CharField(max_length=64)
    title = models.CharField(max_length=255)
    description = models.TextField()
    url_image = models.CharField(max_length=255)
    price_bid = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category_set")
    
    

    def __str__(self):
        return f"{self.title}({self.category})"
    

class Bidding(models.Model):
    title = models.ForeignKey(Auction_Listing, on_delete=models.CASCADE, related_name="title_bids")
    new_bids = models.IntegerField()
    user = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.title}-{self.new_bids}"

class Comment(models.Model):
    title = models.ForeignKey(Auction_Listing, on_delete=models.CASCADE, related_name="title_comments")
    new_comments = models.CharField(max_length=64)
    user = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.title}-{self.new_comments}"

class WatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_watchlist")
    watch_list = models.CharField(max_length=64)

    def __str__(self):
        return self.watch_list

class Auction_Winner(models.Model):
    winner = models.CharField(max_length=64)
    Auction_user = models.CharField(max_length=64)
    title = models.CharField(max_length=64)
    description = models.TextField()
    url_image = models.CharField(max_length=255)
    price_bid = models.IntegerField()
    winner_bid = models.IntegerField()

    def __str__(self):
        return f"{self.title}(winner-{self.winner})"

    


