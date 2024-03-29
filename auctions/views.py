from importlib.resources import contents
from django.contrib.auth import authenticate, login, logout
from .models import AuctionListing
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User


def index(request):
    contents = AuctionListing.objects.all()

    return render(request, "auctions/index.html", {
        "contents": contents,
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


class AuctionItemForm(forms.ModelForm):
    class Meta:
        model = AuctionListing
        fields = ['Title', 'description', 'startingBid', 'imgLinks']

    def __init__(self, *args, **kwargs):
        super(AuctionItemForm, self).__init__(*args, **kwargs)
        self.fields['Title'].widget.attrs.update(
            {'placeholder': 'Enter Title', 'class': 'form-control', 'label': False})
        self.fields['description'].widget.attrs.update(
            {'placeholder': 'Enter Description', 'class': 'form-control', 'label': False})
        self.fields['startingBid'].widget.attrs.update(
            {'placeholder': 'Enter Starting Bid', 'class': 'form-control', 'label': False})
        self.fields['imgLinks'].widget.attrs.update(
            {'placeholder': 'Enter Image Links', 'class': 'form-control', 'label': False})

    Title = forms.CharField(max_length=64, required=True, label='Title')
    description = forms.CharField(
        widget=forms.Textarea(attrs={'maxlength': 200}), required=True, label="Description")
    startingBid = forms.IntegerField(required=True, label="Starting Bid")
    imgLinks = forms.CharField(
        max_length=200, required=True, label="Image Links")


@login_required
def create_Listing(request):

    if request.method == "POST":
        title = request.POST["Title"]
        description = request.POST["description"]
        price = request.POST["startingBid"]
        imageLink = request.POST["imgLinks"]
        user = request.user
        listing = AuctionListing(Title=title, description=description,
                                 startingBid=price,
                                 imgLinks=imageLink, user=user)
        listing.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        form = AuctionItemForm()
        return render(request, "auctions/createListing.html", {
            "form": form,
        })
