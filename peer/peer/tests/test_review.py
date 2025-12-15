from peer.models import Review
from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class ReviewModelTest(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(
            username="reviewer",
            password="pass123",
            email="rev@example.com"
        )
        self.receiver = User.objects.create_user(
            username="reviewed",
            password="pass123",
            email="recv@example.com"
        )

    def test_review_creation(self):
        review = Review.objects.create(
            author=self.author,
            receiver=self.receiver,
            rating=4,
            message="Great experience"
        )

        self.assertEqual(review.author.username, "reviewer")
        self.assertEqual(review.receiver.username, "reviewed")
        self.assertEqual(review.rating, 4)