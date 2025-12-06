from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from peer.models import Listing

User = get_user_model()


class ListingTests(TestCase):
    def test_create_listing_via_view(self):
        # must be logged in to create a listing
        user = User.objects.create_user(username='creator', password='pwd')
        self.client.login(username='creator', password='pwd')
        data = {
            'title': 'Test Offer',
            'description': 'Help with Python',
            'location': 'Local',
            'is_request': False,
            'price': '10.00',
        }
        resp = self.client.post(reverse('create_listing'), data)
        # after creation should redirect to home
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Listing.objects.count(), 1)

    def test_delete_listing_by_author(self):
        # author can delete their listing
        user = User.objects.create_user(username='owner', password='pwd')
        self.client.login(username='owner', password='pwd')
        listing = Listing.objects.create(title='ToDelete', author=user)
        url = reverse('delete_listing', args=[listing.id])
        # GET should show confirmation
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        # POST should delete
        resp = self.client.post(url)
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Listing.objects.filter(id=listing.id).count(), 0)

    def test_delete_listing_by_non_author_forbidden(self):
        owner = User.objects.create_user(username='owner2', password='pwd')
        other = User.objects.create_user(username='other', password='pwd')
        listing = Listing.objects.create(title='KeepMe', author=owner)
        self.client.login(username='other', password='pwd')
        url = reverse('delete_listing', args=[listing.id])
        resp = self.client.post(url)
        # should be forbidden
        self.assertEqual(resp.status_code, 403)
        self.assertEqual(Listing.objects.filter(id=listing.id).count(), 1)
