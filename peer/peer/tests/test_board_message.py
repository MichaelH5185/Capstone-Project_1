from peer.models import BoardMessage, Skill, Board
from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class BoardMessageModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="poster",
            password="pass123",
            email="poster@example.com"
        )
        self.skill = Skill.objects.create(name="AI")
        self.board = Board.objects.create(
            skill=self.skill,
            title="AI Board",
            description="AI discussions",
            creator=self.user
        )

    def test_threaded_reply(self):
        parent = BoardMessage.objects.create(
            poster=self.user,
            content="Original post",
            board=self.board,
            depth=0
        )

        reply = BoardMessage.objects.create(
            poster=self.user,
            content="Reply",
            board=self.board,
            reply_to=parent,
            depth=1
        )

        self.assertEqual(reply.reply_to, parent)
        self.assertEqual(reply.depth, 1)
        self.assertEqual(parent.replies.count(), 1)