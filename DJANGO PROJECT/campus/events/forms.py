from django import forms
from .models import Event, EventRegistration

# Event creation form
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'event_datetime', 'location', 'photo', 'organized_by']
        widgets = {
            'event_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }

# Event registration form
class EventRegistrationForm(forms.ModelForm):
    class Meta:
        model = EventRegistration
        fields = ['name', 'email', 'phone']