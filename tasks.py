from celery import shared_task
from .models import Bid

@shared_task
def test_task():
    print("Test task executed successfully!")

@shared_task
def auto_bid_for_orders():
    """
    Automatically places bids on all available pending orders.
    """
    try:
        pending_orders = Bid.objects.filter(status='Pending')

        # Example: Automatically bid 10% more than the existing bid
        for order in pending_orders:
            bid_amount = order.bid_amount * 1.1  # Bid 10% higher
            Bid.objects.create(
                order_id=order.order_id,
                title=order.title,
                subject=order.subject,
                bid_amount=bid_amount,
                status="Pending",  # Set the status as 'Pending'
            )
        return "Bidding process completed."
    except Exception as e:
        return f"Error in bidding process: {str(e)}"


