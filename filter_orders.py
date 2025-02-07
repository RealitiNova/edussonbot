# filter_orders.py

from .models import Bid  # Make sure you're using the correct model

def filter_orders(subject=None, deadline=None):
    """
    Filters the orders based on subject and/or deadline.
    """
    filtered_orders = Bid.objects.all()  # Get all orders initially

    if subject:
        filtered_orders = filtered_orders.filter(subject__icontains=subject)  # Filter by subject if provided
    if deadline:
        filtered_orders = filtered_orders.filter(deadline__lte=deadline)  # Filter by deadline if provided

    order_list = [
        {"order_id": order.order_id, "subject": order.subject, "title": order.title, "bid_amount": order.bid_amount}
        for order in filtered_orders
    ]

    return order_list
