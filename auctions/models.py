# from turtle import title
from pickle import FALSE
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.BigAutoField(primary_key=True)
    pass


class AuctionListing(models.Model):

    catagories = (
        ('Electronics', 'Electronics'),
        ('Fashion', 'Fashion'),
        ('Home & Garden', 'Home & Garden'),
        ('Collectibles & Art', 'Collectibles & Art'),
        ('Sports & Outdoors', 'Sports & Outdoors'),
        ('Books, Music & Media', 'Books, Music & Media'),
    )
    id = models.BigAutoField(primary_key=True)
    Title = models.CharField(max_length=64)
    description = models.TextField()
    startingBid = models.IntegerField()
    active = models.BooleanField(default=True)
    imgLinks = models.CharField(max_length=200)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="auction_listings")
    category = models.CharField(
        max_length=100, choices=catagories, null=True, default='Home & Garden')
    datListed = models.DateTimeField(auto_now_add=True)

    def formatted_datListed(self):
        return self.datListed.strftime('%B %d, %Y %I:%M %p')


class Bids(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="bids", default=None)
    bid = models.IntegerField(default=0)
    listing = models.ForeignKey(
        AuctionListing, on_delete=models.CASCADE,
        related_name="bids", default=None)


class WatchListing(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="watchlist", default=None)
    isWatchlisted = models.BooleanField(default=False)
    listing = models.ForeignKey(
        AuctionListing, on_delete=models.CASCADE,
        related_name="watchlist", default=None)


class bidWinner(models.Model):
    id = models.BigAutoField(primary_key=True)
    bidWinner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="bidWinner", default=None)
    bidWon = models.ForeignKey(
        AuctionListing, on_delete=models.CASCADE,
        related_name="bidWinner", default=None)
    winning_bid = models.DecimalField(max_digits=10, decimal_places=2)
    date_won = models.DateTimeField(auto_now_add=True)


class comments(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments", default=None)
    comment = models.CharField(max_length=500)
    listing = models.ForeignKey(
        AuctionListing, on_delete=models.CASCADE,
        related_name="comments", default=None)
    datListed = models.DateTimeField(auto_now_add=True)
