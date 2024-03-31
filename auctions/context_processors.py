from django.contrib.auth.decorators import login_required
from .models import AuctionListing, Bids, WatchListing, bidWinner, comments


@login_required
def custom_context(request):
    lists = WatchListing.objects.filter(user=request.user)
    if not lists:
        watchlistCount = 0
    else:
        watchlistCount = lists.count()
    custom_data = {
        'watchlistCount': watchlistCount,
    }
    return custom_data
