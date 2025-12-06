from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from .models import Listing, Message
from .forms import ListingForm, MessageForm, UserRegistrationForm


def home(request):
    listings = Listing.objects.order_by('-created_at')[:20]
    return render(request, 'peer/home.html', {'listings': listings})


@login_required
def create_listing(request):
    if request.method == 'POST':
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            # request.user is authenticated because view is protected
            listing.author = request.user
            listing.save()
            return redirect('home')
    else:
        form = ListingForm()
    return render(request, 'peer/listing_form.html', {'form': form})


def register(request):
    """Register a new user and create their Profile."""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'peer/register.html', {'form': form})


@login_required
def send_message(request, listing_id=None):
    listing = None
    recipient = None
    if listing_id:
        listing = get_object_or_404(Listing, pk=listing_id)
        recipient = listing.author

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
            return redirect('home')
    else:
        form = MessageForm()

    return render(request, 'peer/message_form.html', {'form': form, 'listing': listing})


@login_required
def delete_listing(request, listing_id):
    """Confirm and delete a listing. Only the author may delete their listing."""
    listing = get_object_or_404(Listing, pk=listing_id)
    if listing.author != request.user:
        raise PermissionDenied()

    if request.method == 'POST':
        listing.delete()
        return redirect('home')

    return render(request, 'peer/listing_confirm_delete.html', {'listing': listing})


@login_required
def inbox(request):
    """Display all messages received by the current user."""
    messages = Message.objects.filter(recipient=request.user)\
        .select_related('sender', 'listing')\
        .order_by('-created_at')
    return render(request, 'peer/inbox.html', {'messages': messages})