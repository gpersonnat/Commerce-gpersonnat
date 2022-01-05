from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import Http404

from .models import User, Listing, Bid, Comment, Watchlist
from .forms import createListing, PlaceBid, createComment


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(active=True)
    })


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
def create_listing(request):
    if request.method == "POST":
        form = createListing(request.POST, request.FILES)
        if form.is_valid():
            # Create a new Listing
            listing = Listing(creator_id = request.user.id, name=form.cleaned_data["name"], description = form.cleaned_data["description"], price = form.cleaned_data["price"], image=form.cleaned_data["image"])
            # Insert listing into database
            listing.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/create_listing.html", {
                "form": form
            })
    else:
        return render(request, "auctions/create_listing.html", {
            "form": createListing()
        })

@login_required
def listing(request, id):
    try:
        listing = Listing.objects.get(pk=id)
    except:
        return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(bids__active=True).distinct(),
        "error": "Listing does not exist"
    })
    try:
        comments = listing.comments.all()
    except:
        comments = []
    try:
        highest_bidder = listing.bids.all().order_by('price').reverse()[0].bidder
    except:
        highest_bidder = None
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "active": listing.active,
        "length": len(listing.bids.all()),
        "creator": User.objects.get(pk=(Listing.objects.get(pk=id).creator_id)),
        'form': PlaceBid(),
        "highest_bidder": highest_bidder, 
        "comments": comments
    })


@login_required
def bid(request):
    form = PlaceBid(request.POST)
    listing = Listing.objects.get(pk=request.POST['id'])
    if form.is_valid():
        if form.clean_bid_price(request.POST['id']):
           return render(request, "auctions/listing.html", {
           "listing": listing,
           "length": len(listing.bids.all()),
           "creator": User.objects.get(pk=(Listing.objects.get(pk=request.POST['id']).creator_id)),
           "form": PlaceBid(),
           "error": "Bid is to low"
        })
        bid = Bid(price=form.cleaned_data['price'], bidder=User.objects.get(pk=request.user.id))
        bid.save()
        # Add bid to listing

        listing.bids.add(bid)
        
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/listing.html", {
           "listing": listing,
           "length": len(listing.bids.all()),
           "creator": User.objects.get(pk=(Listing.objects.get(pk=request.POST['id']).creator_id)),
           "form": PlaceBid(),
           "error": "Invalid bid"
        })
        
@login_required
def close_bid(request):
    listing = Listing.objects.get(pk=request.POST['id'])
    listing.update(active=False)
    return HttpResponseRedirect(reverse("index"))

@login_required
def comment(request, id):
    listing = Listing.objects.get(pk=id)
    if request.method == "POST":
        form = createComment(request.POST)
        if form.is_valid():
            comment = Comment(commenter=request.user, text=form.cleaned_data["text"])
            comment.save()
            listing.comments.add(comment)
            return HttpResponseRedirect(reverse("listing", args=(id,)))
        else:
            try:
                highest_bidder = listing.bids.all().order_by('price').reverse()[0].bidder
            except:
                highest_bidder = None
            return render(request, "auctions/listing.html", {
            "listing": listing,
            "active": listing.bids.all()[0].active,
            "length": len(listing.bids.all()),
            "creator": User.objects.get(pk=(Listing.objects.get(pk=id).creator_id)),
            'form': PlaceBid(),
            "highest_bidder": highest_bidder,
            "comment_form": createComment(),
            "error": "Comment is invalid"
        })
    else:
        listing = Listing.objects.get(pk=id)
        try:
            highest_bidder = listing.bids.all().order_by('price').reverse()[0].bidder
        except:
            highest_bidder = None
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "active": listing.active,
            "length": len(listing.bids.all()),
            "creator": User.objects.get(pk=(Listing.objects.get(pk=id).creator_id)),
            'form': PlaceBid(),
            "highest_bidder": highest_bidder,
            "comment_form": createComment()
        })

def watchlist(request):
    if request.method == "POST":
        watchlist_item = Watchlist(watcher=request.user, item=Listing.objects.get(pk=request.POST['listing_id']))
        watchlist_item.save()
        return HttpResponseRedirect("watchlist")
    else:
        return render(request, "auctions/watchlist.html", {
            "watchlist": Watchlist.objects.filter(watcher=request.user)
        })
