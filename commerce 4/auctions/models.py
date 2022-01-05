from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields.related import ManyToManyField


class User(AbstractUser):
    pass

class Comment(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()


class Bid(models.Model):

    # Price of bid
    price = models.DecimalField(max_digits=10, decimal_places=2)

    # Bidder

    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids", default = str(User.objects.get(username="admin")))

    
    def __str__(self):
        return f"{self.id}, {self.bidder}, {self.price}"



class Listing(models.Model):
    # Person who created listing
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_sales")
    
    # Name of Listing
    name = models.CharField(max_length=64)

    # Description of Listing
    description = models.TextField(blank=True)
   
    # Price of Listing
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Image of Listing
    image = models.ImageField(null=True, blank=True, upload_to="images/", default="images/default_image.png")

    # Automatically generates time listing was posted/created
    created_at = models.DateTimeField(auto_now_add=True)

    # Listing that is being bidded on
    bids = models.ManyToManyField(Bid, blank=True, related_name="listing")

    # Comments on Bid
    comments = models.ManyToManyField(Comment, blank=True, related_name="bid")

    active = models.BooleanField(default=True)


    def __str__(self):
        return self.name


class Watchlist(models.Model):
    watcher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watch_items",)
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="watchlist")
