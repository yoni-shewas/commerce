from django.contrib.auth.decorators import login_required
from .models import WatchListing


def custom_context(request):
    custom_data = {}

    if request.user.is_authenticated:
        # The user is logged in
        lists = WatchListing.objects.filter(user=request.user)
        if not lists:
            watchlistCount = 0
        else:
            watchlistCount = lists.count()

        custom_data = {
            'watchlistCount': watchlistCount,
        }

    return custom_data
