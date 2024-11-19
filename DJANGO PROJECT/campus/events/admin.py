from django.contrib import admin
from .models import Event, EventRegistration
from django.utils.html import mark_safe

# EventAdmin: Customize the Event model in the admin interface
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_datetime', 'location', 'organized_by', 'photo_preview')
    list_filter = ('event_datetime', 'location', 'organized_by')  # Filters for the event list
    search_fields = ('title', 'location', 'organized_by')  # Searchable fields
    
    # Show image in the admin list
    def photo_preview(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="50" height="50"/>')
        return "No Image"
    photo_preview.short_description = 'Event Photo'

# EventRegistrationAdmin: Customize the EventRegistration model in the admin interface
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'name', 'email', 'phone')  # Remove registration_date
    list_filter = ('event',)  # Remove registration_date
    search_fields = ('user__username', 'event__title')  # Searchable by user and event title
    readonly_fields = ('user', 'event')  # Remove registration_date

    def has_delete_permission(self, request, obj=None):
        return True  # Prevent deletion of event registrations in the admin interface

# Register the models with the admin site
admin.site.register(Event, EventAdmin)
admin.site.register(EventRegistration, EventRegistrationAdmin)
