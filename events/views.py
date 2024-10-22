# events/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.core.management.base import BaseCommand
from .models import (
    Community,
    Event,
    UnifiedNight,
    Activity,
    Partnership,
    SupportRequest,
    Resource,
    Notification,
    Feedback,
    UserProfile,
    Poll,
    ConnectionRequest,
    DiscussionThread,
    Comment,
    ResourceRequest,
    VolunteerHistory,
    HelpRequest, 
    Thread,
    VolunteerOpportunity, SignUp, PrayerRequest, Reply, CulturalStory, Charity, InitiativeJoin,
 # Import your UserProfile model correctly
)

from .forms import CommunityForm, EventForm, UserRegistrationForm, PartnershipForm, SupportForm, FeedbackForm, PollForm, ConnectionRequestForm, ProfileUpdateForm, ProfileEditForm, PasswordUpdateForm, NotificationPreferencesForm, ProfilePictureForm, CommunityProfileForm, ThreadForm, VolunteerOpportunityForm, SignUpForm, CulturalStoryForm, CharityForm, InitiativeJoinForm,ContactForm, DonationForm

 # Import your forms
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required  # Import login_required
from django.contrib.auth.views import LoginView
from django.utils import timezone
from django.core.paginator import Paginator
from django_otp.decorators import otp_required
from django.core.exceptions import ValidationError
from django.conf import settings
from django.db import IntegrityError
from django.contrib.auth.models import User  # Import the User model
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.views import View
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

from django.http import JsonResponse
import json

import logging

logger = logging.getLogger(__name__)


import openai  # Assuming OpenAI API is used for AI-powered features
import random

def send_otp(email, otp):
    subject = 'Your OTP Code'
    message = f'Your OTP code is: {otp}'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])


def verify_otp(request):
    if request.method == 'POST':
        user_otp = request.POST.get('otp')
        stored_otp = request.session.get('otp')
        username = request.session.get('username')

        if user_otp and stored_otp and int(user_otp) == int(stored_otp):
            # If OTP is valid, log the user in
            user = authenticate(request, username=username)
            if user:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                del request.session['otp']  # Remove OTP from session
                del request.session['username']  # Remove username from session
                return redirect('index')  # Redirect to home
            else:
                messages.error(request, 'Authentication failed.')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')

    return render(request, 'events/verify_otp.html')

@login_required
def index(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    communities = Community.objects.all()
    unified_nights = UnifiedNight.objects.all()
    events = Event.objects.all()
    activities = Activity.objects.all()

    search_query = request.GET.get('search', '')
    if search_query:
        # Ensure you're filtering events using the correct field
        communities = communities.filter(name__icontains=search_query)
        events = events.filter(title__icontains=search_query)

    context = {
        'communities': communities,
        'unified_nights': unified_nights,
        'events': events,
        'activities': activities,
        'search_query': search_query,  # Include the search query in the context
        'user_profile': user_profile,

    }
    return render(request, 'events/index.html', context)


# Authentication Views

# Custom login view
class CustomLoginView(LoginView):
    template_name = 'events/login.html'  # Your login template

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password.')
        return super().form_invalid(form)

# Registration view
def register(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        # Check for empty fields
        if not uname or not email or not pass1 or not pass2:
            messages.error(request, "All fields are required.")
            return redirect('register')

        # Check if the username already exists
        if User.objects.filter(username=uname).exists():
            messages.error(request, "Username already exists. Please choose a different one.")
            return redirect('register')

        # Check if the email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists. Please choose a different one.")
            return redirect('register')

        # Check if passwords match
        if pass1 != pass2:
            messages.error(request, "Your password and confirm password do not match!")
            return redirect('register')

        # Create the user
        try:
            my_user = User.objects.create_user(username=uname, email=email, password=pass1)
            my_user.save()

            # Do not manually create the UserProfile, the post_save signal will handle it
            
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')
        except Exception as e:
            print(f"Error occurred during user registration: {e}")
            messages.error(request, "An error occurred during registration. Please try again.")
            return redirect('register')

    return render(request, 'events/register.html')
# Login view (use Django's built-in view or customize this)

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')  # Ensure this matches the input name in the form

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return HttpResponse("Username or Password is incorrect!!!")

    return render(request, 'events/login.html')


# Logout view
def user_logout(request):
    logout(request)
    return redirect('login')

# Command to create UserProfiles for existing users

# Community Views
@login_required
def about_us(request):
    return render(request, 'events/about_us.html')  # Adjust the template name as necessary
@login_required
def contact(request):
    return render(request, 'events/contact.html')  # Adjust the template name as necessary
@login_required
def profile(request):
    return render(request, 'profile.html')  # Make sure this template exists

 # Ensure only logged-in users can create communities
@login_required
def community_list_view(request):
    communities = Community.objects.all()
    return render(request, 'events/community_list.html', {'communities': communities})

 # Ensure only logged-in users can view community details
@login_required
def community_details_view(request, community_id):
    community = get_object_or_404(Community, id=community_id)
    events = Event.objects.filter(community=community)
    return render(request, 'events/community_details.html', {'community': community, 'events': events})

 # Ensure only logged-in users can create communities
@login_required
def community_create_view(request):
    if request.method == 'POST':
        form = CommunityForm(request.POST)
        if form.is_valid():
            community = form.save(commit=False)
            community.created_by = request.user  # Assign the logged-in user
            community.save()
            messages.success(request, f'Community "{community.name}" created successfully!')
            return redirect('community_detail', community_id=community.id)
    else:
        form = CommunityForm()
    return render(request, 'events/community_form.html', {'form': form})

@login_required
def create_community_profile(request):
    if request.method == 'POST':
        form = CommunityProfileForm(request.POST, request.FILES)
        if form.is_valid():
            community = form.save(commit=False)
            community.save()
            messages.success(request, f'Community profile for {community.name} has been created successfully.')
            return redirect('community_list')  # Redirect to the community list after saving
        else:
            messages.error(request, 'There was an error creating the community profile. Please try again.')
    else:
        form = CommunityProfileForm()

    # Fetch all communities for the dropdown list in the template
    communities = Community.objects.all()

    return render(request, 'events/community_form.html', {
        'form': form,
        'communities': communities,
    })

# Event Views

  # Ensure only logged-in users can view events
@login_required
def event_list_view(request):
    events = Event.objects.all()
    return render(request, 'events/event_list.html', {'events': events})

  # Ensure only logged-in users can view event details
@login_required
def event_details_view(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'events/event_details.html', {'event': event})

  # Ensure only logged-in users can create events
@login_required
def event_create_view(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user  # Assign the logged-in user
            event.save()
            messages.success(request, f'Event "{event.title}" created successfully!')
            return redirect('event_detail', event_id=event.id)
    else:
        form = EventForm()
    return render(request, 'events/event_form.html', {'form': form})

@login_required
def interfaith_networking(request):
    # Fetch communities involved in interfaith activities
    communities = Community.objects.filter(is_interfaith=True)  # Filter communities based on some criteria
    # Fetch upcoming events related to interfaith networking
    events = Event.objects.filter(type='interfaith').order_by('date')  # Assuming you have a 'type' field

    context = {
        'title': 'Interfaith Networking',
        'description': 'Connect with people from different religious backgrounds to share experiences and insights.',
        'communities': communities,
        'events': events,
    }
    
    return render(request, 'events/interfaith_networking.html', context)

@login_required
def create_event_view(request):
    communities = Community.objects.all()  # Fetch all communities

    if request.method == 'POST':
        # Handle form submission with some validation checks
        try:
            title = request.POST['title']
            community_id = request.POST['community']
            location = request.POST['location']
            date = request.POST['date']
            description = request.POST['description']
            organizer = request.user.username  # Organizer is the logged-in user

            # Fetch selected community, raise 404 if not found
            community = Community.objects.get(id=community_id)

            # Convert the date string to datetime if necessary
            try:
                date = timezone.make_aware(timezone.datetime.strptime(date, '%Y-%m-%dT%H:%M'))
            except ValueError:
                messages.error(request, 'Invalid date format. Please try again.')
                return render(request, 'events/event_form.html', {'communities': communities})

            # Create the new event and save it
            event = Event(title=title, location=location, date=date, description=description, organizer=organizer, community=community)
            event.save()
            messages.success(request, 'Event created successfully!')
            return redirect('event_detail', event_id=event.id)

        except Community.DoesNotExist:
            messages.error(request, 'Community does not exist.')
            return render(request, 'events/event_form.html', {'communities': communities})

    return render(request, 'events/create_event.html', {'communities': communities})

@login_required
def partnership_create_view(request):
    if request.method == 'POST':
        form = PartnershipForm(request.POST)
        if form.is_valid():
            partnership = form.save(commit=False)
            partnership.created_by = request.user  # Assign the logged-in user
            partnership.save()
            messages.success(request, 'Partnership created successfully!')
            return redirect('partnership_detail', partnership_id=partnership.id)
    else:
        form = PartnershipForm()
    return render(request, 'events/partnership_form.html', {'form': form})

@login_required
def support_request_view(request):
    if request.method == 'POST':
        form = SupportForm(request.POST)
        if form.is_valid():
            support_request = form.save(commit=False)
            support_request.created_by = request.user  # Assign the logged-in user
            support_request.save()
            messages.success(request, 'Support request submitted successfully!')
            return redirect('support_request_detail', support_request_id=support_request.id)
    else:
        form = SupportForm()
    return render(request, 'events/support_request_form.html', {'form': form})

@login_required
def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user  # Assign the logged-in user
            feedback.save()
            messages.success(request, 'Feedback submitted successfully!')
            return redirect('index')
    else:
        form = FeedbackForm()
    return render(request, 'events/feedback_form.html', {'form': form})

@login_required
def community_delete_view(request, community_id):
    community = get_object_or_404(Community, id=community_id)
    if request.method == 'POST':
        community.delete()
        messages.success(request, 'Community deleted successfully!')
        return redirect('community_list')  # Adjust the redirect as needed
    return render(request, 'events/community_confirm_delete.html', {'community': community})

@login_required
def event_delete_view(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event deleted successfully!')
        return redirect('event_list')  # Adjust the redirect as needed
    return render(request, 'events/event_confirm_delete.html', {'event': event})

@login_required
def ai_response(prompt):
    try:
        openai.api_key = 'your_openai_api_key'  # Use environment variables for sensitive data
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].text.strip()
    except openai.error.OpenAIError as e:
        return "AI is currently unavailable. Please try again later."

@login_required
def ai_chat_view(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input')
        ai_reply = ai_response(user_input)
        return render(request, 'events/ai_chat.html', {'ai_reply': ai_reply, 'user_input': user_input})

    return render(request, 'events/ai_chat.html')

@login_required
def feedback_list_view(request):
    feedbacks = Feedback.objects.all()
    return render(request, 'events/feedback_list.html', {'feedbacks': feedbacks})

@login_required
def notification_list_view(request):
    notifications = Notification.objects.filter(user=request.user)  # Adjust as per your notification model
    return render(request, 'events/notification_list.html', {'notifications': notifications})

@login_required
def resources_view(request):
    resources = Resource.objects.all()
    return render(request, 'events/resources_directory.html', {'resources': resources})


class OfferHelpView(View):
    def get(self, request):
        # Retrieve all previous help offers from the database

        return render(request, 'events/offer_help.html', {
        })

    def post(self, request):
        # Get form data
        user_name = request.POST.get('user_name', '').strip()
        category = request.POST.get('category', '').strip()
        description = request.POST.get('description', '').strip()

        # Validate form data
        if not user_name or not category or not description:
            messages.error(request, 'All fields are required.')
            return redirect('offer_help')  # Redirect back to the same page with an error

        # Save the new offer to the database
        OfferHelp.objects.create(user_name=user_name, category=category, description=description)

        # Show success message
        messages.success(request, 'Your help offer has been submitted successfully!')

        # Redirect to the same page after form submission
        return redirect('offer_help')

      
class RequestHelpView(View):
    def get(self, request):
        help_requests = HelpRequest.objects.all()  # Get all help requests
        help_requests_count = {
            'mental_health': HelpRequest.objects.filter(category='mental_health').count(),
            'food_assistance': HelpRequest.objects.filter(category='food_assistance').count(),
            'shelter_services': HelpRequest.objects.filter(category='shelter_services').count(),
            'educational_support': HelpRequest.objects.filter(category='educational_support').count(),
        }

        return render(request, 'events/request_help.html', {
            'help_requests': help_requests,
            'help_requests_count': help_requests_count,
        })

    def post(self, request):
        # Get form data
        category = request.POST.get('category', '').strip()
        description = request.POST.get('description', '').strip()
        user_name = request.POST.get('user_name', '').strip()

        # Validate the form data
        if not category or not description or not user_name:
            messages.error(request, 'All fields are required.')
            return redirect('request_help')  # Redirect to the same page to display the error

        # Process the form data and save to the database
        HelpRequest.objects.create(category=category, description=description, user_name=user_name)

        # Display success message
        messages.success(request, 'Your help request has been submitted successfully!')

        # Redirect to the same page after successful submission
        return redirect('request_help')

@login_required
def update_status(request, request_id):
    help_request = get_object_or_404(HelpRequest, id=request_id)
    if request.method == "POST":
        help_request.status = not help_request.status  # Toggle the status
        help_request.save()
        messages.success(request, "Help request status updated.")
        return redirect('request_help')

    return render(request, 'update_status.html', {'help_request': help_request})


def view_request_details(request, request_id):
    help_request = get_object_or_404(HelpRequest, id=request_id)
    return render(request, 'request_details.html', {'help_request': help_request})


def request_help_view(request):
    # Get all help requests from the database
    help_requests = HelpRequest.objects.all()  # Adjust the queryset as necessary

    # Process any form submissions if necessary
    if request.method == 'POST':
        # Handle the POST request to create a new help request
        pass

    # Render the template with the help requests
    return render(request, 'request_help.html', {
        'help_requests': help_requests,
        'help_requests_count': help_requests.count(),  # Pass the total count
        'messages': get_messages(request),  # If you are using messages framework
    })


def delete_request_view(request, request_id):
    request_to_delete = get_object_or_404(HelpRequest, id=request_id)
    request_to_delete.delete()
    return redirect('request_help')  # Redirect to the request help page or another page after deletion


def edit_request_view(request, request_id):
    request_to_edit = get_object_or_404(HelpRequest, id=request_id)
    
    if request.method == 'POST':
        # Handle form submission and update logic here
        form = YourForm(request.POST, instance=request_to_edit)  # Replace YourForm with your actual form class
        if form.is_valid():
            form.save()
            return redirect('request_help')
    else:
        form = YourForm(instance=request_to_edit)

    return render(request, 'edit_request.html', {'form': form})  # Adjust template name accordingly

          
class OfferHelpCategoryView(View):
    template_name = 'events/offer_help_category.html'  # Use a common template for all categories

    def get(self, request, category):
        context = {
            'category': category,
        }
        return render(request, self.template_name, context)


class RequestHelpCategory1View(View):
    def get(self, request):
        return render(request, 'events/request_help_category_1.html')


class RequestHelpCategory2View(View):
    def get(self, request):
        return render(request, 'events/request_help_category_2.html')


class RequestHelpCategory3View(View):
    def get(self, request):
        return render(request, 'events/request_help_category_3.html')


class RequestHelpCategory4View(View):
    def get(self, request):
        return render(request, 'events/request_help_category_4.html')

@login_required
def community_networking(request):
    # Retrieve all users in the community excluding the current user
    try:
        users = UserProfile.objects.exclude(user=request.user)
    except UserProfile.DoesNotExist:
        users = []  # Handle case if no UserProfiles are found

    # Retrieve all discussion threads
    threads = Thread.objects.all()  # Assuming you have a Thread model defined

    if request.method == "POST":
        # Handle connection request
        connection_request_form = ConnectionRequestForm(request.POST, user=request.user)  # Pass the user here
        if connection_request_form.is_valid():
            connection_request_form.save()
            return redirect('community_networking')

    # Instantiate form if request is not POST, also pass the user
    connection_request_form = ConnectionRequestForm(user=request.user)  # Pass the user here

    # Pass necessary context to the template
    context = {
        'users': users,
        'threads': threads,  # Add threads to the context
        'connection_request_form': connection_request_form,
    }

    return render(request, 'events/community_networking.html', context)
@login_required
def search_users(request):
    if 'q' in request.GET:
        query = request.GET['q']
        users = UserProfile.objects.filter(user__username__icontains=query)
        return render(request, 'search_results.html', {'users': users})
    return JsonResponse([], safe=False)

@login_required
def create_poll(request):
    if request.method == "POST":
        form = PollForm(request.POST)
        if form.is_valid():
            poll = form.save(commit=False)
            poll.creator = request.user
            poll.save()
            return redirect('community_networking')

    form = PollForm()
    return render(request, 'create_poll.html', {'form': form})

@login_required
def respond_to_poll(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    if request.method == "POST":
        # Handle poll response (e.g., saving the user's vote)
        response = request.POST.get('response')
        poll.votes.create(user=request.user, response=response)
        return redirect('community_networking')

    return render(request, 'respond_to_poll.html', {'poll': poll})

@login_required
def send_connection_request(request, user_id):
    if request.method == "POST":
        user_to_connect = get_object_or_404(UserProfile, id=user_id)
        connection_request = ConnectionRequest(sender=request.user, receiver=user_to_connect.user)
        connection_request.save()
        return JsonResponse({'success': True})

    return JsonResponse({'success': False}, status=400)

# View for the discussion forums page
@login_required
def discussion_forums(request):
    threads = DiscussionThread.objects.all()
    return render(request, 'events/discussion_forums.html', {'threads': threads})

# View for creating a new discussion thread
@login_required
def create_thread(request):
    if request.method == 'POST':
        form = ThreadForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.author = request.user  # Set the author to the current user
            thread.save()
            return redirect('view_thread', thread_id=thread.id)  # Redirect to the thread's detail page
    else:
        form = ThreadForm()
    return render(request, 'create_thread.html', {'form': form})

  # Ensure the user is logged in
@login_required
def view_thread(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    comments = thread.comments.all()  # Get all comments related to the thread

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.thread = thread  # Associate comment with the thread
            comment.author = request.user  # Set the author to the current user
            comment.save()
            return redirect('view_thread', thread_id=thread.id)  # Redirect to the thread's detail page
    else:
        comment_form = CommentForm()

    return render(request, 'view_thread.html', {
        'thread': thread,
        'comments': comments,
        'comment_form': comment_form,
    })

  # Ensure the user is logged in
@login_required
def add_comment(request):
    if request.method == 'POST':
        thread_id = request.POST.get('thread_id')
        thread = get_object_or_404(Thread, id=thread_id)  # Handle thread not found
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.thread = thread
            comment.author = request.user  # Set the author to the current user
            comment.save()
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'fail'})

  # Ensure the user is logged in
def request_resource(request):
    if request.method == 'POST':
        resource_name = request.POST.get('resource_name')
        resource_details = request.POST.get('resource_details')
        new_request = ResourceRequest(name=resource_name, details=resource_details)
        new_request.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'fail'})

@login_required
def profile_edit(request):
    user_profile = request.user.userprofile  # Assuming one-to-one relationship with User model

    if request.method == 'POST':
        try:
            # Check if the request is for updating the profile picture
            if 'profile_picture' in request.FILES:
                update_profile_picture(request, user_profile)
                messages.success(request, "Profile picture updated successfully!")
            else:
                # Update personal information
                update_personal_info(request, user_profile)
                messages.success(request, "Personal information updated successfully!")

            return redirect('profile_view')  # Redirect to a profile view after successful update
        except Exception as e:
            messages.error(request, f"Error updating profile: {e}")

    # GET request: Render the profile edit form
    return render(request, 'events/profile_edit.html', {'user_profile': user_profile})

@csrf_exempt
def update_profile_picture(request):
    if request.method == 'POST':
        try:
            if request.user.is_authenticated:
                user_profile = request.user.userprofile  # Access UserProfile instead of Profile
                if 'profile_picture' in request.FILES:
                    user_profile.profile_picture = request.FILES['profile_picture']
                else:
                    user_profile.profile_picture = 'profile_pictures/default.jpg'  # Default picture if not provided
                user_profile.save()
                return JsonResponse({'success': True, 'message': 'Profile picture updated successfully'})
            else:
                return JsonResponse({'success': False, 'message': 'User is not authenticated'}, status=403)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=400)

@csrf_exempt
def update_personal_info(request):
    if request.method == 'POST':
        user_profile = get_object_or_404(UserProfile, user=request.user)

        try:
            # Update the profile fields
            user_profile.first_name = request.POST.get('first_name', user_profile.first_name)
            user_profile.last_name = request.POST.get('last_name', user_profile.last_name)
            user_profile.bio = request.POST.get('bio', user_profile.bio)
            user_profile.location = request.POST.get('location', user_profile.location)
            user_profile.country = request.POST.get('country', user_profile.country)
            user_profile.state = request.POST.get('state', user_profile.state)
            user_profile.faith_background = request.POST.get('faith_background', user_profile.faith_background)
            user_profile.language = request.POST.get('language', user_profile.language)

            # Handle date of birth (ensure it's a valid date format before assigning)
            dob = request.POST.get('dob')
            if dob:
                user_profile.dob = dob  # Assign the date as a string

            user_profile.gender = request.POST.get('gender', user_profile.gender)

            # Update the username
            new_username = request.POST.get('username', '').strip()
            if new_username and new_username != request.user.username:
                if not User.objects.filter(username=new_username).exists():
                    request.user.username = new_username
                    request.user.save()
                else:
                    return JsonResponse({'success': False, 'message': 'Username already exists.'}, status=400)

            # Save the updated profile
            user_profile.save()

            return JsonResponse({'success': True, 'message': 'Personal information updated successfully!'})
        except Exception as e:
            logger.error(f"Error updating personal info: {e}")
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=400)

def notification_center(request):
    # Query all notifications for the logged-in user, ordered by most recent first
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'events/notifications.html', {
        'notifications': notifications
    })


# View to mark a notification as read (AJAX call)

def mark_as_read(request, notification_id):
    try:
        notification = Notification.objects.get(id=notification_id, user=request.user)
        notification.is_read = True
        notification.save()
        return JsonResponse({'status': 'success'})
    except Notification.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Notification not found'}, status=404)

# View to delete a notification (AJAX call)

def delete_notification(request, notification_id):
    try:
        notification = Notification.objects.get(id=notification_id, user=request.user)
        notification.delete()
        return JsonResponse({'status': 'success'})
    except Notification.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Notification not found'}, status=404)


def settings_view(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)
    user_profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        # Check if the request is for account deletion
        if 'delete_account' in request.POST:
            user.delete()
            messages.success(request, 'Your account has been deleted.')
            return redirect('index')  # Redirect to the home page after deletion

        # Handle profile update
        profile_form = ProfileEditForm(request.POST, instance=profile)
        profile_picture_form = ProfilePictureForm(request.POST, request.FILES, instance=profile)
        notification_form = NotificationPreferencesForm(request.POST)

        if profile_form.is_valid() and profile_picture_form.is_valid() and notification_form.is_valid():
            profile_form.save()
            profile_picture_form.save()
            notification_form.save(user=user)  # Pass user when saving notification preferences

            messages.success(request, 'Profile updated successfully.')
            return redirect('settings')  # Redirect to the settings page after updating

    else:
        profile_form = ProfileEditForm(instance=profile)
        profile_picture_form = ProfilePictureForm(instance=profile)
        notification_form = NotificationPreferencesForm(initial={
            'email_notifications': profile.email_notifications,
            'sms_notifications': profile.sms_notifications,
            'push_notifications': profile.push_notifications,
        })

    context = {
        'user': user,
        'profile_form': profile_form,
        'profile_picture_form': profile_picture_form,
        'notification_form': notification_form,
        'user_profile': user_profile,

    }
    return render(request, 'events/settings.html', context)


def volunteer_opportunities(request):
    opportunities = VolunteerOpportunity.objects.all()

    # Handle Add Opportunity Form
    if request.method == 'POST' and 'add_opportunity' in request.POST:
        add_form = VolunteerOpportunityForm(request.POST)
        if add_form.is_valid():
            add_form.save()
            return redirect('opportunities_list')
    else:
        add_form = VolunteerOpportunityForm()

    # Handle Feedback Form
    if request.method == 'POST' and 'feedback' in request.POST:
        # Process feedback form logic here
        return JsonResponse({'success': True})

    # Initialize SignUpForm for rendering
    sign_up_form = SignUpForm()

    return render(request, 'events/volunteer_opportunities.html', {
        'opportunities': opportunities,
        'add_form': add_form,
        'sign_up_form': sign_up_form,
    })

def sign_up(request, opportunity_id):
    opportunity = get_object_or_404(VolunteerOpportunity, id=opportunity_id)
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            signup = form.save(commit=False)
            signup.opportunity = opportunity
            signup.save()
            opportunity.attendees += 1
            opportunity.save()
            return JsonResponse({'success': True})
    else:
        form = SignUpForm()

    return render(request, 'volunteer/sign_up.html', {
        'form': form, 
        'opportunity': opportunity
    })

@login_required
def profile_view(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    volunteer_history = VolunteerHistory.objects.filter(user=request.user).order_by('-date')

    context = {
        'user_profile': user_profile,
        'volunteer_history': volunteer_history,
    }

    return render(request, 'events/profile.html', context)


# View for editing user profile


# View for adding an activity
@login_required
def add_activity(request):
    if request.method == 'POST':
        form = ActivityForm(request.POST)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.user = request.user
            activity.save()
            return redirect('profile_view')
    else:
        form = ActivityForm()
    return render(request, 'add_activity.html', {'form': form})

# View for listing resources
def resource_list(request):
    resources = Resource.objects.all()
    return render(request, 'events/resource_details.html', {'resources': resources})

# View for adding a resource
@login_required
def add_resource(request):
    if request.method == 'POST':
        form = ResourceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('resource_details')
    else:
        form = ResourceForm()
    return render(request, 'events/resource_directory.html', {'form': form})

# Example of a view for enabling 2FA (if you decide to implement it)
@login_required
def enable_2fa(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        user_profile.is_2fa_enabled = True
        user_profile.save()
        return redirect('profile_view')
    return render(request, 'enable_2fa.html', {'user_profile': user_profile})


def shared_prayer_requests(request):
    return render(request, 'events/shared_prayer_requests.html')  # Adjust the template name as needed

@csrf_exempt  # Remove this in production for security
def submit_prayer(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            prayer_request = PrayerRequest.objects.create(
                prayer_message=data.get('message'),  # Adjust to match your AJAX data
                faith_tradition=data.get('faith_tradition'),  # Adjust to match your AJAX data
                language=data.get('language'),
                is_anonymous=data.get('is_anonymous')  # Adjust to match your AJAX data
            )
            logger.info(f"Prayer created successfully: {prayer_request.id}")
            return JsonResponse({'status': 'success', 'prayer_id': prayer_request.id})

        except json.JSONDecodeError:
            logger.error("Invalid JSON format in the request body.")
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            logger.error(f"Error submitting prayer: {str(e)}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

# View to retrieve all prayer requests
def prayer_feed(request):
    if request.method == 'GET':
        try:
            prayers = PrayerRequest.objects.all().order_by('-created_at')
            prayers_data = [
                {
                    'name': prayer.name if not prayer.is_anonymous else 'Anonymous',
                    'message': prayer.prayer_message,
                    'faith_tradition': prayer.faith_tradition,
                }
                for prayer in prayers
            ]
            return JsonResponse({'prayers': prayers_data}, status=200)

        except Exception as e:
            logger.error(f"Error retrieving prayers: {str(e)}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

@csrf_exempt  # Remove in production for security
def submit_reply(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            prayer_id = data.get('prayer_id')
            reply_message = data.get('reply')  # Ensure this matches your AJAX data

            # Validate input
            if not prayer_id:
                return JsonResponse({'status': 'error', 'message': 'Prayer ID is required'}, status=400)
            if not reply_message:
                return JsonResponse({'status': 'error', 'message': 'Reply message is required'}, status=400)

            # Retrieve the prayer request
            try:
                prayer_request = PrayerRequest.objects.get(id=prayer_id)
            except PrayerRequest.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Prayer request not found'}, status=404)

            # Create the reply
            reply = Reply.objects.create(
                prayer_request=prayer_request,
                message=reply_message
            )
            logger.info(f"Reply created successfully: {reply.id} for prayer ID: {prayer_id}")

            return JsonResponse({'status': 'success', 'reply_id': reply.id}, status=201)

        except json.JSONDecodeError:
            logger.error("Invalid JSON format in the request body.")
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            logger.error(f"Error sending reply: {str(e)}")
            return JsonResponse({'status': 'error', 'message': 'An unexpected error occurred'}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

@login_required
def gamification_elements_view(request):
    # Get the leaderboard sorted by points in descending order
    leaderboard = UserProfile.objects.order_by('-points')[:10]  # Top 10 users
    # Retrieve achievements/badges for the logged-in user
    user_profile = UserProfile.objects.get(user=request.user)

    # You can add any specific achievements or badges logic here
    achievements = []  # Populate this list based on your logic

    return render(request, 'events\gamification_elements.html', {
        'leaderboard': leaderboard,
        'user_profile': user_profile,
        'achievements': achievements,  # This should contain the user's achievements
    })

def share_culture(request):
    thank_you = False
    if request.method == 'POST':
        form = CulturalStoryForm(request.POST, request.FILES)
        if form.is_valid():
            story = form.save(commit=False)
            story.is_approved = False  # Story needs admin approval
            story.save()
            thank_you = True  # Indicate that the user should see a thank-you message
    else:
        form = CulturalStoryForm()

    # Get all stories (both approved and unapproved)
    stories = CulturalStory.objects.all()  # Modify if you want to filter differently

    return render(request, 'events/cultural_exchange.html', {
        'form': form,
        'stories': stories,
        'thank_you': thank_you
    })

def list_cultural_stories(request):
    # Only show approved stories
    stories = CulturalStory.objects.filter(is_approved=True)
    return render(request, 'cultural_stories.html', {'stories': stories})

def thank_you(request):
    return render(request, 'thank_you.html')

def admin_approve_story(request, story_id):
    story = get_object_or_404(CulturalStory, id=story_id)
    story.is_approved = True
    story.save()
    return render(request, 'approval_success.html', {'story': story})

# View to handle all charitable initiatives
@login_required
def charitable_initiatives(request, user_id):
    user_profile = get_object_or_404(UserProfile, id=user_id)
    charities = Charity.objects.all()
    contact_form = ContactForm()
    donation_form = DonationForm()

    if request.method == 'POST':
        # Handle new charity creation
        if 'create_charity' in request.POST:
            charity_name = request.POST.get('charity_name')
            charity_description = request.POST.get('charity_description')
            charity_location = request.POST.get('charity_location')
            founder_name = request.POST.get('founder_name')
            founder_email = request.POST.get('founder_email')

            # Simple validation before saving to the database
            if not all([charity_name, charity_description, charity_location, founder_name, founder_email]):
                return JsonResponse({'success': False, 'message': 'All fields are required.'}, status=400)

            # Create the new Charity
            charity = Charity.objects.create(
                name=charity_name,
                description=charity_description,
                location=charity_location,
                founder_name=founder_name,
                founder_email=founder_email
            )
            return JsonResponse({'success': True, 'message': 'Charity created successfully!'})

        # Handle linking charity to user profile
        elif 'link_charity' in request.POST:
            charity_id = request.POST.get('initiative')
            charity = get_object_or_404(Charity, id=charity_id)

            # Link the charity to the user's profile
            user_profile.initiative = charity
            user_profile.save()
            return JsonResponse({'success': True, 'message': 'Charity linked successfully!'})

        # Handle joining initiatives
        elif 'join_initiative' in request.POST:
            name = request.POST.get('name')
            email = request.POST.get('email')
            message = request.POST.get('message')

            # Basic validation for joining an initiative
            if not all([name, email, message]):
                return JsonResponse({'success': False, 'message': 'Please fill out all the fields.'}, status=400)

            # Save join request in the Contact model
            Contact.objects.create(
                name=name,
                email=email,
                message=message,
                initiative=user_profile.initiative
            )
            return JsonResponse({'success': True, 'message': f'Thank you for joining! {name}'})

        # Handle donations
        elif 'make_donation' in request.POST:
            donation_form = DonationForm(request.POST)
            if donation_form.is_valid():
                donation_form.save()
                return JsonResponse({'success': True, 'message': 'Donation made successfully!'})
            else:
                return JsonResponse({'success': False, 'message': 'Please correct the errors in the donation form.'}, status=400)

    # Handle GET request, return the forms and existing charities
    else:
        form = CharityForm()

    return render(request, 'events/charitable_initiatives.html', {
        'charities': charities,
        'form': form,
        'contact_form': contact_form,
        'donation_form': donation_form,
        'user_profile': user_profile
    })

# View to add a new charity (via POST request)
@csrf_exempt  # For testing purposes; ensure proper CSRF handling in production
def add_charity(request):
    if request.method == 'POST':
        charity_name = request.POST.get('name')
        charity_description = request.POST.get('description')
        charity_location = request.POST.get('location')
        founder_name = request.POST.get('founder')
        founder_email = request.POST.get('founder_email')

        # Validate that all required fields are provided
        if not all([charity_name, charity_description, charity_location, founder_name, founder_email]):
            return JsonResponse({'success': False, 'message': 'All fields are required.'}, status=400)

        # Create and save the new Charity
        charity = Charity.objects.create(
            name=charity_name,
            description=charity_description,
            location=charity_location,
            founder_name=founder_name,
            founder_email=founder_email
        )

        return JsonResponse({'success': True, 'message': 'Charity added successfully!'})

    return JsonResponse({'success': False, 'message': 'Invalid request method. Use POST to add charity.'}, status=400)

# View to handle joining a charitable initiative
@login_required
def join_initiative(request, user_id):
    user_profile = get_object_or_404(UserProfile, id=user_id)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Basic validation
        if not all([name, email, message]):
            return JsonResponse({'success': False, 'message': 'Please fill out all the fields.'}, status=400)

        # Save the join request in the Contact model
        Contact.objects.create(
            name=name,
            email=email,
            message=message,
            initiative=user_profile.initiative
        )
        return JsonResponse({'success': True, 'message': f'Thank you for joining! {name}'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method. Use POST to join an initiative.'}, status=400)

# Contact Form handling to save and store user data
@login_required
def contact_and_save(request):
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)

        if contact_form.is_valid():
            contact_form.save()  # Save the contact details in the database
            return JsonResponse({'success': True, 'message': 'Contact information saved successfully!'})
        else:
            return JsonResponse({'success': False, 'message': 'Invalid form data.'}, status=400)

    return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=400)

@login_required
def interactive_maps(request):
    events = Event.objects.all()  # Fetch all events from the database
    return render(request, 'events/interactive_maps.html', {'events': events})

