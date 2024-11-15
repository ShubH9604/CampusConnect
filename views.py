# events/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from .models import Event, Participation
from .forms import EventForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login
from .models import Event
from django.utils import timezone

# Home page view
def home(request):
    events = Event.objects.filter(event_datetime__gte=timezone.now()).order_by('event_datetime')[:3]
    return render(request, 'home.html', {'events': events})

# List of all events
def events(request):
    events = Event.objects.all().order_by('event_datetime')  # Display all events ordered by datetime
    return render(request, 'events.html', {'events': events})

# Event detail view
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    # Check if the user is already registered for this event
    is_registered = Participation.objects.filter(user=request.user, event=event).exists() if request.user.is_authenticated else False
    
    context = {
        'event': event,
        'is_registered': is_registered
    }
    return render(request, 'event_detail.html', context)

# List of all participations (for the user)
@login_required
def participations(request):
    participations = Participation.objects.filter(user=request.user)
    return render(request, 'participations.html', {'participations': participations})

# About view
def about(request):
    return render(request, 'about.html')

# Create a new event (accessible only by logged-in users)
@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user  # Associate the event with the current logged-in user
            event.save()
            messages.success(request, "Event created successfully!")
            return redirect('events')
    else:
        form = EventForm()
    return render(request, 'create_event.html', {'form': form})

# Update an existing event
@login_required
def update_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if event.user != request.user:
        raise Http404("You are not allowed to edit this event.")

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Event updated successfully!")
            return redirect('events')
    else:
        form = EventForm(instance=event)
    return render(request, 'update_event.html', {'form': form})

# Delete an event
@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if event.user != request.user:
        raise Http404("You are not allowed to delete this event.")

    if request.method == 'POST':
        event.delete()
        messages.success(request, "Event deleted successfully!")
        return redirect('events')
    return render(request, 'delete_event.html', {'event': event})

# Custom login view
def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, "You have successfully logged in!")
                
                # Redirect to the page that user tried to access before login
                next_page = request.GET.get('next', 'home')
                return redirect(next_page)
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

# Register view
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful! Please log in.")
            return redirect('login')  # Redirect to login page after registration
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# Register for event
@login_required
def register_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    # Check if the user is already registered for the event
    if Participation.objects.filter(user=request.user, event=event).exists():
        messages.info(request, f"You are already registered for {event.title}.")
        return redirect('event_detail', event_id=event.id)

    # Register the user for the event
    Participation.objects.create(user=request.user, event=event)
    messages.success(request, f"Successfully registered for {event.title}!")
    return redirect('event_detail', event_id=event.id)
