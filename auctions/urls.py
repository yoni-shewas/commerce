from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('create-listing/', views.create_Listing, name='create-Listing'),
    path('listing/<str:id>/', views.listing_page, name='listing'),
    path('bidding/<str:id>/', views.bidding, name='bidding'),
    path('addWatchlist/<str:id>/', views.add_watchlist, name='addWatchlist'),
    path('closeAuction/<str:id>/', views.close_auction, name='closeAuction'),
    path('Comment/<str:id>/', views.submit_comment, name='submitComment'),
    path('Watchlist', views.WatchList, name='watchlist'),
    path('category/', views.watchCategory, name='categories'),
    path('category/<str:category>/', views.watchCategory, name='category'),
    path('category/', views.watchCategory, name='category'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = 'auctions.views.error_404'
