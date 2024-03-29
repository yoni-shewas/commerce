# from turtle import title
from pickle import FALSE
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.BigAutoField(primary_key=True)
    pass


class AuctionListing(models.Model):
    id = models.BigAutoField(primary_key=True)
    Title = models.CharField(max_length=64)
    description = models.TextField()
    startingBid = models.IntegerField()
    imgLinks = models.CharField(max_length=200)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="auction_listings")


class Bids(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="bids", default=None)
    bid = models.IntegerField(default=0)
    listing = models.ForeignKey(
        AuctionListing, on_delete=models.CASCADE, related_name="bids", default=None)


class WatchListing(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="watchlist", default=None)
    isWatchlisted = models.BooleanField(default=False)
    listing = models.ForeignKey(
        AuctionListing, on_delete=models.CASCADE, related_name="watchlist", default=None)
