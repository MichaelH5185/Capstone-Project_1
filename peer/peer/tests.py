from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Listing, Message, Profile


User = get_user_model()


class ListingMessageTests(TestCase):
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

	def test_send_message_attaches_to_listing(self):
		# create and login a user to send the message
		user = User.objects.create_user(username='msguser', password='pwd')
		self.client.login(username='msguser', password='pwd')
		listing = Listing.objects.create(title='L1')
		url = reverse('send_message', args=[listing.id])
		data = {'sender_name': 'Tester', 'content': 'Hi, I am interested'}
		resp = self.client.post(url, data)
		self.assertEqual(resp.status_code, 302)
		self.assertEqual(Message.objects.count(), 1)
		msg = Message.objects.first()
		self.assertEqual(msg.listing, listing)
		self.assertEqual(msg.sender, user)
		self.assertEqual(msg.sender_name, 'Tester')

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

	def test_anonymous_messaging_requires_name(self):
		listing = Listing.objects.create(title='L-Anonymous')
		url = reverse('send_message', args=[listing.id])
		# anonymous user should be redirected to login when attempting to message
		resp = self.client.post(url, {'sender_name': '', 'content': 'Hi'})
		self.assertEqual(resp.status_code, 302)
		self.assertEqual(Message.objects.count(), 0)


class ProfileTests(TestCase):
	def test_create_profile_model(self):
		# create a user and associated profile
		user = User.objects.create_user(username='profuser', password='pwd')
		Profile.objects.create(
			user=user,
			skills='python, django',
			town='Townsville',
			zipcode='12345',
			state='CA',
		)
		self.assertEqual(Profile.objects.count(), 1)
		p = Profile.objects.get(user=user)
		self.assertEqual(p.skills, 'python, django')
		self.assertEqual(p.town, 'Townsville')
		self.assertEqual(p.zipcode, '12345')
		self.assertEqual(p.state, 'CA')

	def test_register_view_creates_user_and_profile(self):
		url = reverse('register')
		data = {
			'username': 'newuser',
			'password1': 'complexpassword123',
			'password2': 'complexpassword123',
			'skills': 'testing, django',
			'town': 'Smalltown',
			'zipcode': '99999',
			'state': 'TX',
		}
		resp = self.client.post(url, data)
		# after registration we redirect to login
		self.assertEqual(resp.status_code, 302)
		User = get_user_model()
		self.assertTrue(User.objects.filter(username='newuser').exists())
		user = User.objects.get(username='newuser')
		self.assertTrue(Profile.objects.filter(user=user).exists())
		p = Profile.objects.get(user=user)
		self.assertEqual(p.skills, 'testing, django')
		self.assertEqual(p.town, 'Smalltown')
		self.assertEqual(p.zipcode, '99999')
		self.assertEqual(p.state, 'TX')
