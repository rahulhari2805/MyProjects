from django.urls import path

from . import views

urlpatterns = [
    path("index", views.index, name="index"),
    path("index/<str:listing>", views.auctionlist, name="auctionlist"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_list", views.create_list, name="create_list"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("category_list/", views.category_list, name="category_list"),
    path("category_list/<str:cat>", views.auction_category, name="auction_category")
    
    
    
    
    
   
]
