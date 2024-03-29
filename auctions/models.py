# from turtle import title
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
        User, on_delete=models.CASCADE, related_name="person")


class Bids(models.Model):
    id = models.BigAutoField(primary_key=True)
    pass
    pass


class Listing(models.Model):
    id = models.BigAutoField(primary_key=True)
    pass
