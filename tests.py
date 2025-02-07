from django.test import TestCase
from django.contrib.auth.models import User
from .models import Bid, UserProfile, BidHistory


class BidModelTest(TestCase):
    def setUp(self):
        self.bid = Bid.objects.create(
            order_id="12345",
            title="Sample Order",
            subject="Mathematics",
            bid_amount=50.00,
            status="Pending"
        )

    def test_bid_creation(self):
        self.assertEqual(self.bid.title, "Sample Order")
        self.assertEqual(self.bid.status, "Pending")
        self.assertEqual(float(self.bid.bid_amount), 50.00)

class UserProfileTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.profile = UserProfile.objects.create(user=self.user, phone_number="+1234567890", notifications_enabled=True)

    def test_user_profile_creation(self):
        self.assertEqual(self.profile.user.username, "testuser")
        self.assertEqual(self.profile.phone_number, "+1234567890")
        self.assertTrue(self.profile.notifications_enabled)

class BidHistoryTest(TestCase):
    def setUp(self):
        self.bid = Bid.objects.create(
            order_id="12345",
            title="Sample Order",
            subject="Mathematics",
            bid_amount=50.00,
            status="Pending"
        )
        self.history = BidHistory.objects.create(
            bid=self.bid,
            previous_status="Pending",
            new_status="Accepted"
        )

    def test_bid_history_creation(self):
        self.assertEqual(self.history.previous_status, "Pending")
        self.assertEqual(self.history.new_status, "Accepted")
        self.assertEqual(self.history.bid.order_id, "12345")