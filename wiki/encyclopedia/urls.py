from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("<str:entry>", views.entries, name="entry"),
    path("search/<str:entry>", views.entries, name="entry"),
    path("search/", views.search, name="search"),
    
    path("create/", views.create, name="create"),
    path("edit/<str:page_edit>/", views.edit, name="edit")
    
    
    
    ]
