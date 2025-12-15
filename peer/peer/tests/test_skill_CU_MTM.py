from django.test import TestCase
from django.contrib.auth import get_user_model
from peer.models import Skill

User = get_user_model()

class SkillUserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="skilluser",
            password="pass123",
            email="skill@example.com"
        )

        self.skill1 = Skill.objects.create(name="Python")
        self.skill2 = Skill.objects.create(name="Django")

    def test_user_skill_assignment(self):
        self.user.skills.add(self.skill1, self.skill2)

        self.assertEqual(self.user.skills.count(), 2)
        self.assertIn(self.skill1, self.user.skills.all())
        self.assertIn(self.skill2, self.user.skills.all())