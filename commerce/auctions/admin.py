from django.contrib import admin


from .models import User, Category, Auction_Listing, Bidding, Comment, WatchList, Auction_Winner

# Register your models here.
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Auction_Listing)
admin.site.register(Bidding)
admin.site.register(Comment)
admin.site.register(WatchList)
admin.site.register(Auction_Winner)