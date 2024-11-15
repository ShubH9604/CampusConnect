# events/admin.py

from django.contrib import admin
from .models import Event, Participation

# Register the Event model in the admin panel
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'event_datetime', 'location', 'photo')  # Display these fields in the list view
    search_fields = ('title', 'location')  # Add search functionality for title and location
    list_filter = ('event_datetime', 'user')  # Filter events by date and user
    ordering = ('event_datetime',)  # Default ordering by event datetime

# Register the Participation model in the admin panel
class ParticipationAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'registered_at')  # Display these fields in the list view
    search_fields = ('user__username', 'event__title')  # Search by username and event title
    list_filter = ('event',)  # Filter by event

# Register models with custom admin views
admin.site.register(Event, EventAdmin)
admin.site.register(Participation, ParticipationAdmin)
