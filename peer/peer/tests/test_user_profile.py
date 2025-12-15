from peer.models import Profile
from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="profileuser",
            password="pass123",
            email="profile@example.com"
        )

    def test_profile_creation(self):
        profile = Profile.objects.create(
            user=self.user,
            town="Madison",
            state="WI",
            about="Computer science student"
        )

        self.assertEqual(profile.user.username, "profileuser")
        self.assertEqual(profile.town, "Madison")
        self.assertEqual(profile.state, "WI")