from django.db import models
from datetime import date
from django.conf import settings

# Create your models here.
class Chat(models.Model):
    created_at = models.DateField(default=date.today)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_chats',
        default=None
    )
    partners = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='chats',
    )

class Message(models.Model):
    text = models.CharField(max_length=500)
    created_at = models.DateField(default=date.today)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='author_message_set'
    )
    chat = models.ForeignKey(
        Chat,
        on_delete=models.CASCADE,
        related_name='chat_message_set',
        default=None,
        blank=True,
        null=True
    )