from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:id>", views.listing, name="listing"),
    path("comment/<int:id>", views.comment, name="comment"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("bid", views.bid, name="bid"),
    path("close_bid", views.close_bid, name="close_bid"),
    path("watchlist", views.watchlist, name="watchlist")
]
