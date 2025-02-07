from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import IntegrityError
from django.db import models

class Order(models.Model):
    # Fields here
    pass


# Model representing a Bid placed on an order
class Bid(models.Model):
    order_id = models.CharField(max_length=100, unique=True)  # Unique identifier for the order
    title = models.CharField(max_length=255)  # Title of the order
    subject = models.CharField(max_length=255)  # Subject of the order (e.g., Programming, Design)
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)  # Amount of the bid
    status = models.CharField(
        max_length=50, 
        choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')], 
        default='Pending'  # Default status is 'Pending'
    )
    timestamp = models.DateTimeField(auto_now_add=True)  # Timestamp for when the bid was placed

    def __str__(self):
        return f"Order {self.order_id} - {self.title} - {self.bid_amount}$ ({self.status})"

# Model representing User Profile with additional preferences like notifications enabled
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    notifications_enabled = models.BooleanField(default=True)  # User preference for receiving notifications

    def __str__(self):
        return self.user.username

# Model to track changes in Bid Status (Bid History)
class BidHistory(models.Model):
    bid = models.ForeignKey(Bid, on_delete=models.CASCADE, related_name='history')
    updated_at = models.DateTimeField(auto_now=True)  # When the status was updated
    previous_status = models.CharField(max_length=50)  # Previous status before the update
    new_status = models.CharField(max_length=50)  # New status after the update

    def __str__(self):
        return f"Bid {self.bid.order_id} changed from {self.previous_status} to {self.new_status}"

# Function to place a bid on an order automatically
def place_bid_for_order(user, order_id, bid_amount):
    """
    Places a bid automatically on a pending order.
    """
    try:
        # Fetch the order using order_id (assuming order_id is unique)
        order = Bid.objects.get(order_id=order_id, status='Pending')

        # Create a bid for the user
        bid = Bid.objects.create(
            order_id=order_id,
            title=order.title,
            subject=order.subject,
            bid_amount=bid_amount,
            status='Pending',  # You can adjust the status or leave it as Pending
            timestamp=timezone.now()
        )

        # Track the status change in the BidHistory
        BidHistory.objects.create(
            bid=bid,
            previous_status='Pending',
            new_status='Pending'
        )

        # Optionally, you can update the order's status if necessary
        order.status = 'Accepted'  # Example: Automatically accept the bid
        order.save()

        # Log the status change for the order in history
        BidHistory.objects.create(
            bid=order,
            previous_status='Pending',
            new_status='Accepted'
        )

        return bid
    except Bid.DoesNotExist:
        return None  # Order not found, handle gracefully
    except IntegrityError:
        return None  # Handle error if bid creation fails due to integrity issues

# Function to automatically place bids on all eligible orders
def auto_bid_for_orders():
    """
    Queries all orders marked as 'Pending' and automatically places bids.
    """
    # Retrieve all orders that are 'Pending'
    pending_orders = Bid.objects.filter(status='Pending')

    # Retrieve users who have automatic bidding enabled (without sensitive info)
    users = UserProfile.objects.filter(notifications_enabled=True)

    # Iterate over each user and place bids on the available orders
    for user_profile in users:
        for order in pending_orders:
            # Implement your bidding logic (e.g., bid 10% higher than the existing bid)
            bid_amount = order.bid_amount * 1.1  # Example: bid 10% higher than the existing bid
            place_bid_for_order(user_profile.user, order.order_id, bid_amount)

    return "Bidding process completed."
