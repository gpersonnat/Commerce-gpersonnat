from django.contrib import admin

from .models import User, Listing, Bid, Comment, Watchlist

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display= ("id", "username", "email",)

class ListingAdmin(admin.ModelAdmin):
    list_display = ("id","name")

admin.site.register(User, UserAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Watchlist)