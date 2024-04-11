from datetime import timezone
from importlib.resources import contents
from logging import PlaceHolder
from multiprocessing import Value
from unicodedata import category
from django.contrib.auth import authenticate, login, logout
from .models import AuctionListing, Bids, WatchListing, bidWinner, comments
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from .models import User


def index(request):
    contents = AuctionListing.objects.filter(active=True)

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

    catagories = (
        ('Electronics', 'Electronics'),
        ('Fashion', 'Fashion'),
        ('Home & Garden', 'Home & Garden'),
        ('Collectibles & Art', 'Collectibles & Art'),
        ('Sports & Outdoors', 'Sports & Outdoors'),
        ('Books, Music & Media', 'Books, Music & Media'),
    )

    class Meta:
        model = AuctionListing
        fields = ['Title', 'description',
                  'startingBid', 'imgLinks', 'category']

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
        self.fields['category'].widget.attrs.update(
            {'placeholder': 'choose category', 'class': 'form-control', 'label': False})

    Title = forms.CharField(max_length=64, required=True, label='Title')
    description = forms.CharField(
        widget=forms.Textarea(attrs={'maxlength': 200}), required=True, label="Description")
    startingBid = forms.IntegerField(required=True, label="Starting Bid")
    imgLinks = forms.CharField(
        max_length=200, required=True, label="Image Links")
    category = forms.ChoiceField(
        choices=catagories, required=True, label="Category")


class BidForm(forms.ModelForm):
    class Meta:
        model = Bids
        fields = ['bid']
    bid = forms.IntegerField(required=True)

    def __init__(self, *args, **kwargs):
        initial_values = kwargs.pop('initial_values', None)
        self.bid_constraint = kwargs.pop('bid_constraint', None)
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

    def clean_bid(self):
        bid = self.cleaned_data.get("bid")

        # Check if bid is empty
        if bid is None:
            raise forms.ValidationError('Bid cannot be empty')

        # Add more constraints as needed
        # For example, to check if bid is greater than bid_constraint
        if self.bid_constraint is not None and bid <= self.bid_constraint:
            raise forms.ValidationError(
                f'Bid must be greater than {self.bid_constraint}')

        return bid


class commentForm(forms.ModelForm):
    class Meta:
        model = comments
        fields = ['comment']

    comment = forms.CharField(
        widget=forms.Textarea(attrs={'maxlength': 500}),
        required=True,
        label="Comment"
    )

    def __init__(self, *args, **kwargs):
        # Call parent class's __init__ method
        super(commentForm, self).__init__(*args, **kwargs)
        self.fields['comment'].widget.attrs.update(
            {'placeholder': 'Enter your comment here',
                'class': 'form-control', 'rows': 4}
        )


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
    user = request.user
    bids = Bids.objects.filter(listing=listing)
    bid_count = bids.count()
    maxBids = bids.order_by('-bid').first()

    commentF = commentForm()
    commentList = comments.objects.filter(listing=listing)

    if maxBids is not None:
        maxBid = maxBids.bid
    else:
        maxBid = 0
    try:
        bid_win = bidWinner.objects.get(bidWon=listing)
    except bidWinner.DoesNotExist:
        bid_win = None
    if bid_win and bid_win.bidWinner.id == user.id:
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "user": user,
            "bid_win": bid_win,
            "bid_count": bid_count,
            "max_bid": maxBid,
            "commentForm": commentF,
            "commentList": commentList,
        })

    else:
        try:
            # Use get() to directly retrieve the WatchListing object
            Watchlist = WatchListing.objects.get(user=user, listing=listing)
        except WatchListing.DoesNotExist:
            # Create a new WatchListing object if it doesn't exist
            watchlisted = WatchListing(
                user=request.user, isWatchlisted=False, listing=listing)
            watchlisted.save()
            Watchlist = WatchListing.objects.get(user=user, listing=listing)

        print(f"{maxBid} {maxBids}")
        initial_data = {'bid': bid_count, }
        starting_Bid = {'bid_constraint': int(listing.startingBid)}
        form = BidForm(initial_values=initial_data,
                       bid_constraint=starting_Bid)
        print(Watchlist.isWatchlisted)

        return render(request, "auctions/listing.html", {
            "listing": listing,
            "form": form,
            "user": user,
            "bid_win": bid_win,
            "bid_count": bid_count,
            "max_bid": maxBid,
            "commentForm": commentF,
            "commentList": commentList,
            "Watchlist": Watchlist,
        })


@login_required
def bidding(request, id):
    listing = get_object_or_404(AuctionListing, id=id)

    if request.method == "POST":
        form = BidForm(request.POST, bid_constraint=listing.startingBid)
        print(request.POST)
        if form.is_valid():
            bid = form.save(commit=False)
            bid.listing = listing
            bid.user = request.user
            bid.save()
            return HttpResponseRedirect(reverse("listing", args=[id]))
    else:
        form = BidForm(bid_constraint=listing.startingBid)

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "form": form,
    })


@login_required
def add_watchlist(request, id):
    listing = get_object_or_404(AuctionListing, id=id)

    if request.method == "POST":
        try:
            # Use get() to directly retrieve the WatchListing object
            Watchliste = WatchListing.objects.get(
                listing=listing, user=request.user)

            # Update the object if it exists
            if Watchliste.isWatchlisted:
                Watchliste.isWatchlisted = False
            else:
                Watchliste.isWatchlisted = True
            Watchliste.save()
        except WatchListing.DoesNotExist:
            # Create a new WatchListing object if it doesn't exist
            watchlisted = WatchListing(
                user=request.user, isWatchlisted=True, listing=listing)
            watchlisted.save()

        return HttpResponseRedirect(reverse("listing", args=[id]))


@login_required
def close_auction(request, id):
    listing = get_object_or_404(AuctionListing, id=id)
    bids = Bids.objects.filter(listing=listing)
    if request.method == 'POST':
        if listing.active:
            listing.active = False
            listing.save()
            maxBidder = bids.order_by('-bid').first()
            if maxBidder:
                winning_bid = maxBidder.bid
                bid_winner = bidWinner.objects.create(
                    bidWinner=maxBidder.user,
                    bidWon=listing,
                    winning_bid=winning_bid,
                )
                bid_winner.save()

        return HttpResponseRedirect(reverse("listing", args=[id]))


@login_required
def submit_comment(request, id):
    listing = get_object_or_404(AuctionListing, id=id)

    if request.method == 'POST':
        form = commentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.listing = listing
            comment.save()
        print(form.is_valid())

        return HttpResponseRedirect(reverse("listing", args=[id]))


def WatchList(request):
    lists = WatchListing.objects.filter(user=request.user)

    return render(request, "auctions/watchlist.html", {
        "contents": lists,
    })


def watchCategory(request, category=None):
    if category is not None:
        lists = AuctionListing.objects.filter(
            category=category, active=True)
        return render(request, "auctions/category.html", {
            "contents": lists,
            "category": category,
        })
    else:
        return render(request, "auctions/category.html", {
            "contents": [],
            "category": None,
        })


@login_required
def user_panel(request):
    """User Panel view: shows all auctions that user:
        * is currently selling
        * sold
        * is currently bidding
        * won
    """
    # Helpers
    all_distinct_bids = Bids.objects.filter(
        user=request.user.id).values_list("listing", flat=True).distinct()
    won = []

    # Get auctions currently being sold by the user
    selling = AuctionListing.objects.filter(
        active=False, user=request.user.id).order_by("-datListed").all()

    # Get auction sold by the user
    sold = AuctionListing.objects.filter(
        active=True, user=request.user.id).order_by("-datListed").all()

    # Get auctions currently being bid by the user
    bidding = AuctionListing.objects.filter(
        active=False, id__in=all_distinct_bids).all()

    # Get auctions won by the user
    for auction in AuctionListing.objects.filter(active=True, id__in=all_distinct_bids).all():
        highest_bid = Bids.objects.filter(
            listing=auction.id).order_by('-bid').first()

        if highest_bid.user.id == request.user.id:
            won.append(auction)

    return render(request, "auctions/user_panel.html", {
        "selling": selling,
        "sold": sold,
        "bidding": bidding,
        "won": won
    })


def error_404(request, exception):
    return render(request, '404.html', status=404)
