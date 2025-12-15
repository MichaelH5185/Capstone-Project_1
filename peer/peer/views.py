from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages

from .models import Listing, Message, Skill, CustomUser
from .forms import ListingForm, MessageForm, UserRegistrationForm


def home(request):
    listings = Listing.objects.order_by('-created_at')[:20]
    return render(request, 'peer/home.html', {'listings': listings})


def view_listings(request):
    """Display all listings with a button to create new ones."""
    listings = Listing.objects.order_by('-created_at')
    return render(request, 'peer/listings.html', {'listings': listings})


@login_required
def create_listing(request):
    if request.method == 'POST':
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            # request.user is authenticated because view is protected
            listing.author = request.user
            listing.save()
            return redirect('peer:home')
    else:
        form = ListingForm()
    return render(request, 'peer/listing_form.html', {'form': form})


def register(request):
    """Register a new user and create their Profile."""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('peer:login')
    else:
        form = UserRegistrationForm()
    return render(request, 'peer/register.html', {'form': form})


@login_required
def send_message(request, listing_id=None, recipient_id=None, message_id=None):
    listing = None
    recipient = None
    
    if message_id:
        # Reply to an existing message
        original_message = get_object_or_404(Message, pk=message_id)
        recipient = original_message.sender
        listing = original_message.listing  # Inherit listing from original message
    elif listing_id:
        listing = get_object_or_404(Listing, pk=listing_id)
        recipient = listing.author
    elif recipient_id:
        recipient = get_object_or_404(CustomUser, pk=recipient_id)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            # Sender must be the authenticated user (login_required ensures this)
            msg.sender = request.user
            if not msg.sender_name:
                msg.sender_name = request.user.username

            if recipient:
                msg.recipient = recipient
            if listing:
                msg.listing = listing
            msg.save()
            return redirect('peer:inbox')
    else:
        form = MessageForm()

    return render(request, 'peer/message_form.html', {'form': form, 'listing': listing, 'recipient': recipient})


@login_required
def delete_listing(request, listing_id):
    """Confirm and delete a listing. Only the author may delete their listing."""
    listing = get_object_or_404(Listing, pk=listing_id)
    if listing.author != request.user:
        raise PermissionDenied()

    if request.method == 'POST':
        # Delete all messages related to this listing
        Message.objects.filter(listing=listing).delete()
        # Delete the listing
        listing.delete()
        return redirect('peer:home')

    return render(request, 'peer/listing_confirm_delete.html', {'listing': listing})


@login_required
def inbox(request):
    """Display all messages received by the current user."""
    messages_list = Message.objects.filter(recipient=request.user).select_related('sender', 'listing').order_by('-created_at')
    return render(request, 'peer/inbox.html', {'messages_list': messages_list})


def create_new_skill(request):
    """Create a new skill."""
    if request.method == "POST":
        name = request.POST.get("name")
        if Skill.objects.filter(name=name).exists():
            messages.error(request, "Skill Already Exists")
            return redirect("peer:create-skill")
        Skill.objects.create(name=name)
        messages.success(request, f"Skill '{name}' created successfully!")
        return redirect("peer:home")
    return render(request, "skills/create_skill.html")
