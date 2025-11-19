from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Listing(models.Model):
    """A skill listing or a request posted by a user."""
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="listings",
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    is_request = models.BooleanField(
        default=False,
        help_text="If true this is a request, otherwise an offer",
    )
    price = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({'Request' if self.is_request else 'Offer'})"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    skills = models.CharField(max_length=300, blank=True)
    town = models.CharField(max_length=100, blank=True)
    zipcode = models.CharField(max_length=20, blank=True)
    state = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"Profile for {self.user.username}"

class Message(models.Model):
    """A simple message optionally attached to a Listing."""
    sender = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sent_messages",
    )
    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="received_messages",
    )
    listing = models.ForeignKey(
        Listing,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="messages",
    )
    sender_name = models.CharField(
        max_length=150,
        blank=True,
        help_text="Optional name when sender is anonymous",
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        sender_label = (
            self.sender_name or (self.sender.username if self.sender else "Anon")
        )
        return f"Message from {sender_label}"
