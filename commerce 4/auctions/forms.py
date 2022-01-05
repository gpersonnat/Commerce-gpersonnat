from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import Listing, Bid, User, Comment
from django.shortcuts import render

class createListing(ModelForm):
    class Meta:
        model = Listing
        fields = ['name', 'description', 'price', 'image']

class PlaceBid(ModelForm):
    
    class Meta:
        model = Bid
        fields = ['price']

    def __init__(self, *args, **kwargs):
        
        super(PlaceBid, self).__init__(*args, **kwargs)
        self.fields['price'].widget.attrs['placeholder'] = 'Bid'
    
    def clean_bid_price(self, id):
        '''Check if bid is lower than starting bid'''
        data = self.cleaned_data['price']
        listing = Listing.objects.get(pk=id)
        bids = listing.bids.all()
        if not bids:
            return False
        if float(data) < float(bids.order_by('price').reverse()[0].price):
            return True
        return False
 
class createComment(ModelForm):
    class Meta:
        model = Comment 
        fields = ['text']
    
    def __init__(self, *args, **kwargs):
        super(createComment, self).__init__(*args, **kwargs)
        self.fields['text'].widget.attrs['placeholder'] = 'Comment'
        self.fields['text'].label = ''