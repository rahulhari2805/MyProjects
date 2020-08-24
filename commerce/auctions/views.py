from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Avg, Max, Min, Sum
from django.contrib.auth.decorators import login_required


from .models import User, Category, Auction_Listing, Bidding, Comment, WatchList, Auction_Winner



def index(request):
    
    bid_winner = Auction_Winner.objects.filter(winner=request.user.get_username())
    
    if request.method == "POST":
        new_list = Auction_Listing.objects.get(title=request.POST.get("get_watchlist"))
        get_watchlist = WatchList.objects.filter(user=request.user)
        
        check_list = []
        for watch in get_watchlist:
            check_list += Auction_Listing.objects.filter(title=watch)

        if new_list in check_list:
            context = {"auctions" : Auction_Listing.objects.all(), "exists" : "Watchlist Already Added", "bid_winner" : bid_winner}
            return render(request, "auctions/index.html", context)

        else:
            new_watchlist = WatchList(user=request.user, watch_list=new_list.title)
            new_watchlist.save()
            return HttpResponseRedirect("watchlist")

    
     
            
    context = {"auctions" : Auction_Listing.objects.all(), "bid_winner" : bid_winner}
    return render(request, "auctions/index.html", context)


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

@login_required
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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create_list(request):
    
    template = "auctions/createlist.html"
    
    if request.method == "POST":
        
        user = request.user
        title = request.POST.get("title")
        description = request.POST.get("description")
        price_bid = request.POST.get("price_bid")
        image_url = request.POST.get("image_url")
        category = request.POST.get("category")

        categories = Category(user=user, category=category)
        categories.save()

        auction = Auction_Listing(Auction_user=request.user.get_username(), title=title, description=description, url_image=image_url, price_bid=price_bid)
        auction.category = categories
        auction.save()

        bid_auction = Auction_Listing.objects.get(title=title)
        bids = Bidding(title=bid_auction, new_bids=price_bid, user=request.user.get_username())
        bids.save()
        
        return HttpResponseRedirect(reverse("index"))

    return render(request, template)


@login_required
def watchlist(request):
    template = "auctions/watchlist.html"
    get_watchlist = WatchList.objects.filter(user=request.user)
    get_auctionlist = []
    
    for watch in get_watchlist:
        get_auctionlist += Auction_Listing.objects.filter(title=watch)
        
    if request.method == "POST":
        remove_watchlist = WatchList.objects.get(user=request.user, watch_list=request.POST.get("remove_watchlist"))
        remove_watchlist.delete()
        return HttpResponseRedirect("watchlist")
            
    context = {"auction" : get_auctionlist}
    return render(request, template, context)


def auctionlist(request, listing):

    auctions = Auction_Listing.objects.get(title=listing)
    comments_list = Comment.objects.filter(title=auctions)
    bids_list = Bidding.objects.filter(title=auctions).aggregate(Max("new_bids"))
    max_value = bids_list["new_bids__max"]
    
    auction_user = auctions.Auction_user
    
    if request.method == "POST":
        if request.POST.get("get_watchlist") != listing and request.POST.get("close_auction") != "closeauction":
            if request.POST.get("new_comment") != "":
                comments = Comment(title=auctions, new_comments=request.POST.get("new_comment"), user=request.user.get_username())
                comments.save()
                content = {"auctions" : auctions, "comments" : comments_list, "bids" : max_value, "closeauction" : auction_user == request.user.get_username()}
                return render(request, "auctions/auctionlist.html", content)

            if request.POST.get("new_bid") != "":
                if int(request.POST.get("new_bid")) <= int(max_value):
                    content = {"auctions" : auctions, "comments" : comments_list, "bids" : max_value, "warn" : "Enter higher than highest priced bid/Base bid", "closeauction" : auction_user == request.user.get_username()}
                    return render(request, "auctions/auctionlist.html", content)
                
                else:
                    bids = Bidding(title=auctions, new_bids=request.POST.get("new_bid"), user=request.user.get_username())
                    bids.save()
                    bids_list1 = Bidding.objects.filter(title=auctions).aggregate(Max("new_bids"))
                    max_value1 = bids_list1["new_bids__max"]
                    content = {"auctions" : auctions, "comments" : comments_list, "bids" : max_value1, "success" : "Your Bid has been raised", "closeauction" : auction_user == request.user.get_username()}
                    return render(request, "auctions/auctionlist.html", content)

        else:
            if request.POST.get("close_auction") == "closeauction":
                bid_winner = Bidding.objects.filter(title=auctions).aggregate(Max("new_bids"))
                winner_bid = bid_winner["new_bids__max"]
                select_winner = Bidding.objects.get(title=auctions, new_bids=winner_bid)

                save_winner = Auction_Winner(winner=select_winner.user, Auction_user=auction_user, title=auctions.title,
                                                  description=auctions.description, url_image=auctions.url_image, price_bid=auctions.price_bid, winner_bid=winner_bid)
                save_winner.save()
                auctions.delete()
                
                content = {"auctions" : auctions, "comments" : comments_list, "bids" : max_value, "closeauction" : auction_user == request.user.get_username()}
                return render(request, "auctions/auctionlist.html", content)
                
            else:
                new_list = Auction_Listing.objects.get(title=request.POST.get("get_watchlist"))
                get_watchlist = WatchList.objects.filter(user=request.user)
                
                check_list = []
                for watch in get_watchlist:
                    check_list += Auction_Listing.objects.filter(title=watch)
                if new_list in check_list:
                    content = {"auctions" : auctions, "comments" : comments_list, "bids" : max_value, "exists" : "Watchlist Already Added", "closeauction" : auction_user == request.user.get_username()}
                    return render(request, "auctions/auctionlist.html", content)
                
                else:
                    new_watchlist = WatchList(user=request.user, watch_list=new_list.title)
                    new_watchlist.save()
                    return HttpResponseRedirect(reverse("watchlist"))

    content = {"auctions" : auctions, "comments" : comments_list, "bids" : max_value, "closeauction" : auction_user == request.user.get_username()}
    return render(request, "auctions/auctionlist.html", content)


def category_list(request):
    
    template = "auctions/category_list.html"
    return render(request, template)


def auction_category(request, cat):
    template = "auctions/auction_category.html"

    cat_list = Category.objects.filter(category=cat)
    cats_list = []
    for cat in cat_list:
        cats_list += Auction_Listing.objects.filter(category=cat)
    
    content = {"catlist" : cats_list, "categoryhead" : cat}

    return render(request, template, content)







