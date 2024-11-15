# events/models.py

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Linking event to a user
    title = models.CharField(max_length=255)  # Event title
    description = models.TextField()  # Detailed event description
    event_datetime = models.DateTimeField(default=timezone.now)  # Date and time of event
    location = models.CharField(max_length=255)  # Location of the event
    photo = models.ImageField(upload_to='events/photos/', blank=True, null=True)  # Optional photo for event

    def __str__(self):
        return f"{self.title} on {self.event_datetime.strftime('%Y-%m-%d %H:%M')}"
    
class Participation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} registered for {self.event.title} on {self.registered_at.strftime('%Y-%m-%d %H:%M')}"
