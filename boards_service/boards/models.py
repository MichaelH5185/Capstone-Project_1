from django.db import models

class Board(models.Model):
    skill = models.IntegerField(null=True)
    sub_skill = models.CharField(max_length=50)
    creator = models.IntegerField(null=True, related_name="creator")
    created = models.DateTimeField(auto_now_add=True)
    moderator = models.IntegerField(null=True, related_name="moderator")
    name = models.TextField()

class BoardMessage(models.Model):
    poster = models.IntegerField(null=True)
    reply_to = models.ForeignKey("self", on_delete=models.SET_NULL, related_name="Replies", null=True)
    content = models.TextField()
    time_posted = models.DateTimeField(auto_now_add=True)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, null=False)