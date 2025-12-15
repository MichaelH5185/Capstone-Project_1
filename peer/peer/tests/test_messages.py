from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from peer.models import Listing, Message

User = get_user_model()


class MessageTests(TestCase):
    def test_send_message_attaches_to_listing(self):
        # create and login a user to send the message
        user = User.objects.create_user(username='msguser', password='pwd', email="msguser@gmail.com")
        self.client.login(username='msguser', password='pwd')
        listing = Listing.objects.create(title='L1', author=user)
        url = reverse('peer:send_message', args=[listing.id])
        data = {'sender_name': 'Tester', 'content': 'Hi, I am interested'}
        resp = self.client.post(url, data)
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Message.objects.count(), 1)
        msg = Message.objects.first()
        self.assertEqual(msg.listing, listing)
        self.assertEqual(msg.sender, user)
        self.assertEqual(msg.sender_name, 'Tester')

    def test_anonymous_messaging_requires_login(self):
        user = User.objects.create_user(username='msguser2', password='pwd', email="msguser2@gmail.com")
        self.client.login(username='msguser2', password='pwd')
        listing = Listing.objects.create(title='L-Anonymous', author=user)
        self.client.logout()
        url = reverse('peer:send_message', args=[listing.id])
        # anonymous user should be redirected to login when attempting to message
        resp = self.client.post(url, {'sender_name': '', 'content': 'Hi'})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Message.objects.count(), 0)

    def test_inbox_shows_received_messages(self):
        # Create two users
        sender = User.objects.create_user(username='sender', password='pwd', email="sender@gmail.com")
        recipient = User.objects.create_user(username='recipient', password='pwd', email="recipient@gmail.com")
        
        # Create messages sent to recipient
        Message.objects.create(
            sender=sender,
            recipient=recipient,
            content='Message 1',
            sender_name='sender'
        )
        Message.objects.create(
            sender=sender,
            recipient=recipient,
            content='Message 2',
            sender_name='sender'
        )
        
        # Create a message NOT sent to recipient
        other_user = User.objects.create_user(username='other3', password='pwd', email="other3@gmail.com")
        Message.objects.create(
            sender=sender,
            recipient=other_user,
            content='Message for someone else',
            sender_name='sender'
        )
        
        # Login as recipient and view inbox
        self.client.login(username='recipient', password='pwd')
        resp = self.client.get(reverse('inbox'))
        
        # Should be successful
        self.assertEqual(resp.status_code, 200)
        
        # Should only show messages for this recipient (2 messages)
        self.assertEqual(len(resp.context['messages']), 2)
        
        # Verify messages contain correct content
        messages = list(resp.context['messages'])
        self.assertIn('Message 1', [m.content for m in messages])
        self.assertIn('Message 2', [m.content for m in messages])

    def test_inbox_requires_login(self):
        self.client.logout()
        # Anonymous user should be redirected to login
        resp = self.client.get(reverse('peer:inbox'))
        self.assertEqual(resp.status_code, 302)
        self.assertIn('/accounts/login/', resp.url)

    def test_inbox_empty_for_user_with_no_messages(self):
        # Create user with no messages
        user = User.objects.create_user(username='lonely', password='pwd', email='lonely@gmail.com')
        self.client.login(username='lonely', password='pwd')
        
        resp = self.client.get(reverse('inbox'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['messages']), 0)
