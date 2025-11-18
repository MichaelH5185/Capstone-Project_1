from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser

class Skill(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False)
    
class CustomUser(AbstractUser):
    username = models.CharField(max_length=50, null=False, unique=True)
    rating = models.FloatField(default=5)
    skills = models.ManyToManyField(Skill, blank=True)
    rating_count = models.IntegerField(default=0)
    
#Should we change it so that if the user that created the listing is deleted it deletes the posting?
class Listing(models.Model):
    """A skill listing or a request posted by a user."""
    author = models.ForeignKey(
        CustomUser,
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


class Message(models.Model):
    """A simple message optionally attached to a Listing."""
    sender = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sent_messages",
    )
    recipient = models.ForeignKey(
        CustomUser,
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
 
class Review(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name="reviews_received")
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False)
    message = models.CharField(max_length=200, null=True, blank=True)
    rating = models.IntegerField(default=5)
    time_created = models.DateTimeField(auto_now_add=True)
    
class Profile(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False)
    
class Board(models.Model):
    skill = models.ForeignKey(Skill, on_delete=models.SET_NULL, null=True)
    sub_skill = models.CharField(max_length=50)
    creator = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)

class BoardMessage(models.Model):
    poster = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    reply_to = models.ForeignKey("self", on_delete=models.SET_NULL, related_name="Replies", null=True)
    content = models.TextField()
    time_posted = models.DateTimeField(auto_now_add=True)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, null=False)