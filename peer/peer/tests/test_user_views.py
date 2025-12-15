from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from peer.models import Skill, Profile

User = get_user_model()

class LoginBehaviorTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="loginuser",
            email="login@test.com",
            password="pass123"
        )

    def test_user_can_login_with_email(self):
        response = self.client.post(
            reverse("user:login"),
            {
                "email": "login@test.com",
                "password": "pass123"
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("peer:home"))

    def test_login_fails_with_wrong_password(self):
        response = self.client.post(
            reverse("user:login"),
            {
                "email": "login@test.com",
                "password": "wrongpass"
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "incorrect")

class RegisterBehaviorTest(TestCase):
    def setUp(self):
        self.skill = Skill.objects.create(name="Python")

    def test_user_can_register(self):
        response = self.client.post(
            reverse("user:register"),
            {
                "username": "newuser",
                "email": "new@test.com",
                "password": "pass123",
                "password2": "pass123",
                "skills": [self.skill.id],
            }
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_password_mismatch_blocks_registration(self):
        response = self.client.post(
            reverse("user:register"),
            {
                "username": "baduser",
                "email": "bad@test.com",
                "password": "pass123",
                "password2": "pass456",
            }
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(username="baduser").exists())
        
class ProfileCreationBehaviorTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="profileuser",
            password="pass123",
            email="profile@test.com"
        )
        self.client.login(username="profileuser", password="pass123")

    def test_user_can_create_profile(self):
        response = self.client.post(
            reverse("user:create_profile"),
            {
                "fname": "John",
                "lname": "Doe",
                "town": "Madison",
                "state": "WI",
                "zip": "53703",
                "about_me": "CS student"
            }
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Profile.objects.filter(user=self.user).exists())

class ViewProfileBehaviorTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="viewer",
            password="pass123",
            email="viewer@test.com"
        )
        self.client.login(username="viewer", password="pass123")

    def test_redirect_to_create_profile_if_missing(self):
        response = self.client.get(
            reverse("user:view_profile", kwargs={"uid": self.user.id})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("user:create_profile"))

from peer.models import Review

class ReviewBehaviorTest(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(
            username="sender",
            password="pass123",
            email="sender@test.com"
        )
        self.receiver = User.objects.create_user(
            username="receiver",
            password="pass123",
            email="receiver@test.com"
        )

        self.client.login(username="sender", password="pass123")

        # Ensure review object exists for your view logic
        Review.objects.create(
            author=self.sender,
            receiver=self.receiver,
            rating=5,
            message="Initial"
        )

    def test_user_can_leave_review(self):
        response = self.client.post(
            reverse("user:leave_review", kwargs={"uid": self.receiver.id}),
            {
                "rating": 4,
                "review": "Good experience"
            }
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            Review.objects.filter(receiver=self.receiver).count(),
            1
        )

class LogoutBehaviorTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="logoutuser",
            password="pass123",
            email="logout@test.com"
        )
        self.client.login(username="logoutuser", password="pass123")

    def test_user_can_logout(self):
        response = self.client.get(reverse("user:logout"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("user:login"))