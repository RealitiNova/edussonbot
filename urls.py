from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from .views import chat_with_gpt, get_orders, start_bidding, track_bids
from django.shortcuts import render
from django.http import JsonResponse
from .tasks import auto_bid_for_orders

# ✅ Redirect to Edusson Login
def external_login(request):
    return redirect('https://edusson.com/writer')

# ✅ Define URL Patterns
urlpatterns = [
    # Core views
    path('', views.home_view, name='home'),  # Home page
    path('login/', views.login_view, name='login'),  # User login
    path('signup/', views.signup_view, name='signup'),  # User signup
    path('dashboard/', views.dashboard_view, name='dashboard'),  # Dashboard
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Logout
    path('accounts/', include('django.contrib.auth.urls')),  # Auth URLs

    # External login redirection
    path('external-login/', external_login, name='external_login'),

    path('fetch-orders/', views.fetch_orders_view, name='fetch_orders'),  # Fetch orders view
    # other paths

    path('filter-orders/', views.filter_orders, name='filter_orders'),  # Filter orders based on criteria
    path('submit-bid/', views.submit_bid, name='submit_bid'),  # Submit a bid on an order
    path('start-auto-bidding/', views.start_auto_bidding, name='start_auto_bidding'),  # Trigger auto-bidding process


    # View to trigger the Celery task for auto-bidding
def start_auto_bidding(request):
    try:
        # Trigger the Celery task asynchronously
        auto_bid_for_orders.delay()  # Use .delay() to call the Celery task asynchronously
        return JsonResponse({"message": "Auto-bidding process started."}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

    # Auto-bidding
    path('start-auto-bidding/', views.start_auto_bidding, name='start_auto_bidding'),

    # ChatGPT Integration
    path('chat/', chat_with_gpt, name='chat_with_gpt'),

    # API Endpoints for Bidding Bot
    path('api/orders/', get_orders, name='get_orders'),  # Fetch available orders
    path('api/start-bid/', start_bidding, name='start_bidding'),  # Start bidding process
    path('api/track-bids/', track_bids, name='track_bids'),  # Track bid status
    path('generate-bid/', views.generate_bid_view, name='generate_bid'),  # URL for generating a bid
    # other URLs
    path('save-settings/', views.save_settings, name='save_settings'),  # URL for saving settings
    # other URL patterns
]

from django.urls import path
from . import views

urlpatterns = [
    # Add this path to link the "Place Bids for New Orders" button
    path('place_bids_for_new_orders/', views.place_bids_for_new_orders, name='place_bids_for_new_orders'),
    # Other existing routes...
]


urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    # Other URLs...
]
