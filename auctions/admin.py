from django.contrib import admin
from .models import User, AuctionListing, Bids

# Register your models here.


admin.site.register(User)
admin.site.register(AuctionListing)
admin.site.register(Bids)
