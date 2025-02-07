from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import logging

from .models import auto_bid_for_orders  # Ensure this model is correctly implemented
from .chatbot import chatgpt_response
from .fetch_orders import fetch_orders
from .filter_orders import filter_orders
from .generate_bid import generate_bid
from .submit_bid import submit_bid

from django.shortcuts import render
from django.http import JsonResponse
from .models import Bid
from .tasks import auto_bid_for_orders


# Configure logging
logger = logging.getLogger(__name__)

# ✅ Home View
def home_view(request):
    return render(request, 'edusson_app/home.html')

# ✅ Signup View
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Signup failed. Please check the form.")
    else:
        form = UserCreationForm()
    
    return render(request, 'edusson_app/signup.html', {'form': form})

# ✅ Login View
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid credentials. Please try again.")
    else:
        form = AuthenticationForm()
    
    return render(request, 'edusson_app/login.html', {'form': form})

# ✅ Logout View
def logout_view(request):
    logout(request)
    return redirect('home')

# ✅ Dashboard View
@login_required
def dashboard_view(request):
    if request.method == "POST":
        try:
            message = auto_bid_for_orders()  # Auto-bid function
            messages.success(request, message)
        except Exception as e:
            messages.error(request, f"Error during auto-bidding: {e}")
            logger.error(f"Auto-bidding error: {e}")
        
        return redirect('dashboard')

    return render(request, 'edusson_app/dashboard.html')

    # View to fetch orders from the platform
def fetch_orders_view(request):
    try:
        orders = fetch_orders()  # Call the function to fetch orders using Selenium
        return JsonResponse({"orders": orders}, status=200)  # Return orders in JSON format
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)  # Handle errors gracefully

# View to filter orders based on subject or deadline
def filter_orders(request):
    subject = request.GET.get("subject", None)  # Filter by subject (if provided)
    deadline = request.GET.get("deadline", None)  # Filter by deadline (if provided)

    # Filter orders based on subject and/or deadline
    filtered_orders = Bid.objects.all()

    if subject:
        filtered_orders = filtered_orders.filter(subject__icontains=subject)  # Case-insensitive match for subject
    if deadline:
        filtered_orders = filtered_orders.filter(deadline__lte=deadline)  # Filter by deadline (before or equal to)

    orders_list = [
        {"order_id": order.order_id, "subject": order.subject, "title": order.title, "bid_amount": order.bid_amount}
        for order in filtered_orders
    ]

    return JsonResponse({"filtered_orders": orders_list}, status=200)

# View to trigger auto-bidding task
def start_auto_bidding(request):
    try:
        # Triggering the background task to place bids automatically
        auto_bid_for_orders()  # This calls the function or Celery task that automates the bidding process
        return JsonResponse({"message": "Auto-bidding process started."}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# ✅ Manually Trigger Auto-Bidding
def start_auto_bidding(request):
    try:
        auto_bidding_message = auto_bid_for_orders()
        return HttpResponse(auto_bidding_message)
    except Exception as e:
        logger.error(f"Error starting auto-bidding: {e}")
        return HttpResponse(f"Error: {e}", status=500)

# ✅ ChatGPT Integration
@csrf_exempt
def chat_with_gpt(request):
    if request.method == "POST":
        user_message = request.POST.get("message", "")
        subject_name = request.POST.get("subject", "General Studies")

        if not user_message:
            return JsonResponse({"error": "Message cannot be empty"}, status=400)

        bot_reply = chatgpt_response(user_message, subject_name)
        return JsonResponse({"response": bot_reply})

    return JsonResponse({"error": "Invalid request"}, status=400)

# ✅ Fetch Available Orders from Edusson
@csrf_exempt
def get_orders(request):
    if request.method == "GET":
        try:
            orders = fetch_orders()  # Fetch orders from Edusson
            return JsonResponse({"orders": orders})
        except Exception as e:
            logger.error(f"Error fetching orders: {e}")
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)

# ✅ Start Bidding Process
@csrf_exempt
def start_bidding(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            order_id = data.get("order_id")
            subject = data.get("subject")

            if not order_id or not subject:
                return JsonResponse({"error": "Missing order_id or subject"}, status=400)

            bid_message = generate_bid(subject)
            success = submit_bid(order_id, bid_message)

            if success:
                return JsonResponse({"message": "Bid submitted successfully", "order_id": order_id})
            else:
                return JsonResponse({"error": "Failed to submit bid"}, status=500)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except Exception as e:
            logger.error(f"Error during bidding: {e}")
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)

# View to submit a bid on an order
def submit_bid(request):
    if request.method == "POST":
        order_id = request.POST.get("order_id")
        bid_amount = request.POST.get("bid_amount")

        if not order_id or not bid_amount:
            return JsonResponse({"error": "Order ID and bid amount are required."}, status=400)

        # Create a bid for the order
        try:
            order = Bid.objects.get(order_id=order_id)
            bid = Bid.objects.create(
                order_id=order_id,
                title=order.title,
                subject=order.subject,
                bid_amount=bid_amount,
                status="Pending",  # Set the status to pending when creating the bid
            )
            return JsonResponse({"message": "Bid submitted successfully.", "bid_id": bid.id}, status=201)
        except Bid.DoesNotExist:
            return JsonResponse({"error": "Order not found."}, status=404)
    return JsonResponse({"error": "Invalid request method."}, status=400)


# ✅ Track Bids Status
@csrf_exempt
def track_bids(request):
    if request.method == "GET":
        try:
            bid_statuses = track_bid_status()  # Fetch bid statuses
            return JsonResponse({"bids": bid_statuses})
        except Exception as e:
            logger.error(f"Error tracking bids: {e}")
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)

# generate_bid.py

from django.http import JsonResponse
from .generate_bid import generate_bid  # Assuming generate_bid is defined in a separate file

def generate_bid_view(request):
    """
    View to generate a new bid for an order. It receives order_id, subject, and current_bid_amount
    and returns a new bid amount.
    """
    # Get the necessary parameters from the request (GET or POST)
    order_id = request.GET.get('order_id')  # Or use POST, depending on how you want to send data
    subject = request.GET.get('subject')
    current_bid_amount = request.GET.get('current_bid_amount')

    # Validate the parameters
    if not order_id or not subject or not current_bid_amount:
        return JsonResponse({"error": "Missing required parameters (order_id, subject, current_bid_amount)."}, status=400)
    
    try:
        current_bid_amount = float(current_bid_amount)  # Convert the bid amount to a float
    except ValueError:
        return JsonResponse({"error": "Invalid current_bid_amount, must be a number."}, status=400)

    if current_bid_amount <= 0:
        return JsonResponse({"error": "Invalid bid amount, it must be greater than 0."}, status=400)

    # Generate the new bid amount using the external function (e.g., from OpenAI or logic)
    try:
        new_bid_amount = generate_bid(subject, current_bid_amount)  # Assuming generate_bid function handles the logic
    except Exception as e:
        return JsonResponse({"error": f"Error generating bid: {str(e)}"}, status=500)

    # Return the new bid amount as a response
    return JsonResponse({"order_id": order_id, "subject": subject, "new_bid_amount": new_bid_amount}, status=200)


# Inside the view or function where chat_with_gpt is used
def some_view(request):
    from edusson_app.views import chat_with_gpt  # Import inside the function to avoid circular import
    # Now you can use chat_with_gpt without circular import
    chat_with_gpt(request)

def save_settings(request):
    """
    View to handle saving settings (e.g., user preferences).
    """
    if request.method == 'POST':
        # Example: Handling 'notifications_enabled' checkbox from the form
        notifications_enabled = request.POST.get('notifications_enabled') == 'on'  # Convert to boolean
        
        try:
            # Logic to save the settings (you could save it to the UserProfile model)
            # Example: Assuming you have a UserProfile model
            # user_profile = UserProfile.objects.get(user=request.user)
            # user_profile.notifications_enabled = notifications_enabled
            # user_profile.save()

            return JsonResponse({"message": "Settings saved successfully."}, status=200)

        except Exception as e:
            return JsonResponse({"error": f"Error saving settings: {str(e)}"}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=400)

