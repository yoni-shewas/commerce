from importlib.resources import contents
from logging import PlaceHolder
from multiprocessing import Value
from django.contrib.auth import authenticate, login, logout
from .models import AuctionListing, Bids, WatchListing
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

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


class BidForm(forms.ModelForm):
    class Meta:
        model = Bids
        fields = ['bid']

    def __init__(self, *args, **kwargs):
        initial_values = kwargs.pop('initial_values', None)
        super(BidForm, self).__init__(*args, **kwargs)

        if initial_values:
            for field_name, value in initial_values.items():
                if field_name in self.fields:
                    self.fields[field_name].widget.attrs.update(
                        {'placeholder': 'Enter Bid', 'class': 'form-control'})
                    Label = str(value) + \
                        ' bid(s) so far, Your bid is the current bid'
                    self.fields[field_name].label = Label
            for field_name, field in self.fields.items():
                self.fields[field_name].widget.attrs['placeholder'] = "Enter Bid"

    bid = forms.IntegerField(required=True)


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
        return HttpResponseRedirect(reverse("listing", args=[listing.id]))
    else:
        form = AuctionItemForm()
        return render(request, "auctions/createListing.html", {
            "form": form,
        })


@login_required
def listing_page(request, id):
    listing = get_object_or_404(AuctionListing, id=id)
    bids = Bids.objects.filter(listing=listing)
    bid_count = bids.count()

    initial_data = {'bid': bid_count}
    form = BidForm(initial_values=initial_data)

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "form": form,
    })


@login_required
def bidding(request, id):
    listing = get_object_or_404(AuctionListing, id=id)

    if request.method == "POST":
        form = BidForm(request.POST)
        print(request.POST)
        if form.is_valid():
            bid = form.save(commit=False)
            bid.listing = listing
            bid.user = request.user
            bid.save()
            return HttpResponseRedirect(reverse("listing", args=[id]))
        else:
            try:
                form.clean_bid()
            except ValidationError as e:
                return HttpResponseBadRequest(e.message)
    else:
        # Redirect to the listing page if the request method is not POST
        return HttpResponseRedirect(reverse("listing", args=[id]))


@login_required
def add_watchlist(request, id):
    listing = get_object_or_404(AuctionListing, id=id)

    if request.method == "POST":
        try:
            # Use get() to directly retrieve the WatchListing object
            isWatchlisted = WatchListing.objects.get(listing=listing)

            # Update the object if it exists
            if isWatchlisted.isWatchlisted:
                isWatchlisted.isWatchlisted = False
            else:
                isWatchlisted.isWatchlisted = True
            isWatchlisted.save()
        except WatchListing.DoesNotExist:
            # Create a new WatchListing object if it doesn't exist
            watchlisted = WatchListing(
                user=request.user, isWatchlisted=True, listing=listing)
            watchlisted.save()

        return HttpResponseRedirect(reverse("listing", args=[id]))
