from django.db import models
from users.models import User

class Conversation(models.Model):
    DIRECTION_CHOICES = [('user', 'User'), ('llm', 'LLM')]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    direction = models.CharField(max_length=10, choices=DIRECTION_CHOICES)

    def __str__(self):
        return f"{self.user.name} ({self.direction})"
