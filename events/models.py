from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_2fa_enabled = models.BooleanField(default=False)
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    faith_background = models.CharField(max_length=255, blank=True, null=True)
    interests = models.TextField(blank=True, null=True)
    social_links = models.URLField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', default='default.jpg')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email_verified = models.BooleanField(default=False)
    email = models.EmailField(max_length=254, unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    email_notifications = models.BooleanField(default=False)
    sms_notifications = models.BooleanField(default=False)
    push_notifications = models.BooleanField(default=False)
    community = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    volunteering_details = models.TextField(blank=True)
    interfaith_interests = models.TextField(blank=True)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following', blank=True)
    points = models.IntegerField(default=0)
    badges = models.JSONField(default=list)
    initiative = models.ForeignKey('Charity', related_name='participants', on_delete=models.CASCADE)

    # New fields added
    language = models.CharField(max_length=50, blank=True, null=True)  # Language preference
    dob = models.DateField(blank=True, null=True)  # Date of birth
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], blank=True, null=True)  # Gender options

    def __str__(self):
        return f'{self.user.username} Profile'


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(
            user=instance,
            email=instance.email,
            first_name=instance.first_name,
            last_name=instance.last_name
        )
    else:
        user_profile = instance.userprofile
        user_profile.email = instance.email
        user_profile.first_name = instance.first_name
        user_profile.last_name = instance.last_name
        user_profile.save()

class Community(models.Model):
    # Choices for community type
    COMMUNITY_TYPE_CHOICES = [
        ('Religious', 'Religious'),
        ('Social', 'Social'),
        ('Educational', 'Educational'),
    ]
    
    # Community Information
    name = models.CharField(max_length=255, unique=True)  # Ensuring community names are unique
    description = models.TextField()
    
    # Contact Details
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=15)  # Adjust length based on your requirements
    
    # Location Information
    address = models.CharField(max_length=255)
    location = models.CharField(max_length=255)  # Landmark or general location
    worship_house_name = models.CharField(max_length=255)  # e.g., Church, Temple, Mosque
    map_location = models.URLField()  # Google Maps URL
    
    # Community Members
    members = models.TextField(blank=True)  # Store member names as a comma-separated string
    suggest_members = models.TextField(blank=True)  # Store suggested member names
    
    # Worship Details
    worship_details = models.TextField(blank=True)  # Additional details about the worship house
    
    # Community Type and Interfaith Status
    community_type = models.CharField(max_length=50, choices=COMMUNITY_TYPE_CHOICES)
    is_interfaith = models.BooleanField(default=False)
    
    # Media Files
    profile_image = models.ImageField(upload_to='community_profiles/', blank=True)  # Community profile image
    logo = models.ImageField(upload_to='community_logos/', null=True, blank=True)  # Community logo
    
    # Social Media Links
    facebook_link = models.URLField(blank=True)
    twitter_link = models.URLField(blank=True)
    instagram_link = models.URLField(blank=True)
    
    # User Information and Timestamps
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)  # Establish relationship with User
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)  # Allow nulls temporarily
    updated_at = models.DateTimeField(auto_now=True)  # Auto-update timestamp when modified

    def __str__(self):
        return self.name


class Event(models.Model):
    EVENT_TYPE_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
        ('interfaith', 'Interfaith'),
    ]

    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    date = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=200)
    description = models.TextField()
    organizer = models.CharField(max_length=100)
    max_participants = models.PositiveIntegerField(null=True, blank=True)
    rsvp_deadline = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=EVENT_TYPE_CHOICES, default='public')

    def clean(self):
        if self.date and self.date < timezone.now():
            raise ValidationError('Event date cannot be in the past.')
        if self.rsvp_deadline and self.date and self.rsvp_deadline >= self.date:
            raise ValidationError('RSVP deadline must be before the event date.')

    def __str__(self):
        return f"{self.title} ({self.community.name})"

class UnifiedNight(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    location = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Activity(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    description = models.TextField(blank=True)
    location = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

class Partnership(models.Model):
    community = models.ForeignKey(Community, related_name='partnerships', on_delete=models.CASCADE)
    partner_name = models.CharField(max_length=100)
    partnership_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)  # Track when the partnership ends
    description = models.TextField()

    def __str__(self):
        return self.partner_name

class SupportRequest(models.Model):
    community = models.ForeignKey(Community, related_name='support_requests', on_delete=models.CASCADE)
    user_name = models.CharField(max_length=100)
    request_date = models.DateTimeField(auto_now_add=True)
    request_details = models.TextField()
    status = models.CharField(max_length=50, default='Pending')  # Track status of request

    def __str__(self):
        return f"Support Request by {self.user_name}"

class Resource(models.Model):
    community = models.ForeignKey(Community, related_name='resources', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    file_upload = models.FileField(upload_to='uploads/', null=True, blank=True)  # Make this nullable if required
    link = models.URLField(blank=True, null=True)  # Allow this to be blank or null if the resource is a file
    resource_type = models.CharField(max_length=100, blank=True, null=True)  # Type of resource

    def __str__(self):
        return self.title

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255, default="Untitled")
    message = models.TextField()
    notification_type = models.CharField(max_length=50, default='General')  # Type of notification
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Notification for {self.user.username}: {self.title}'

class Feedback(models.Model):
    community = models.ForeignKey(Community, related_name='feedbacks', on_delete=models.CASCADE)
    user_name = models.CharField(max_length=100)
    feedback_date = models.DateTimeField(auto_now_add=True)
    feedback_text = models.TextField()
    rating = models.PositiveIntegerField(default=0)  # Rating field for feedback

    def __str__(self):
        return f"Feedback from {self.user_name}"

class Poll(models.Model):
    question = models.CharField(max_length=255)
    options = models.JSONField()  # Store options for the poll
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question

class PollResponse(models.Model):
    poll = models.ForeignKey(Poll, related_name='votes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    response = models.CharField(max_length=255)

    class Meta:
        unique_together = ('poll', 'user')  # Ensure one response per user for each poll

    def __str__(self):
        return f"{self.user.username} voted on {self.poll.question}"

class ConnectionRequest(models.Model):
    sender = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username} connection request"

class DiscussionThread(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  # Set the default user ID
    community = models.ForeignKey(Community, related_name='discussion_threads', on_delete=models.CASCADE, default=1)  # Provide a default community ID

    def __str__(self):
        return self.title

class Thread(models.Model):
    title = models.CharField(max_length=200)  # Title of the thread
    content = models.TextField()               # Content of the thread
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set on creation
    updated_at = models.DateTimeField(auto_now=True)      # Automatically set on update
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the User who created the thread

    def __str__(self):
        return self.title

class Comment(models.Model):
    thread = models.ForeignKey(DiscussionThread, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  # Provide a default user ID
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.created_by} on {self.thread.title}"

class HelpRequest(models.Model):
    CATEGORY_CHOICES = [
        ('mental_health', 'Mental Health Support'),
        ('food_assistance', 'Food Assistance'),
        ('shelter_services', 'Shelter Services'),
        ('educational_support', 'Educational Support'),
    ]

    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField()
    user_name = models.CharField(max_length=100, null=True, blank=True)  # Allow null values
    email = models.EmailField(max_length=254, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)  # True if fulfilled, False otherwise


    def __str__(self):
        return f"{self.category}: {self.description[:50]}..."

class OfferHelp(models.Model):
    CATEGORY_CHOICES = [
        ('mental_health', 'Mental Health Support'),
        ('food_assistance', 'Food Assistance'),
        ('shelter_services', 'Shelter Services'),
        ('educational_support', 'Educational Support'),
    ]

    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField()
    user_name = models.CharField(max_length=100, null=True, blank=True)  # Allow null values
    email = models.EmailField(max_length=254, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)  # True if fulfilled, False otherwise

    def __str__(self):
        return f"{self.category}: {self.description[:50]}..."


class ResourceRequest(models.Model):
    name = models.CharField(max_length=255)
    details = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Pending')  # Track the status of the request

    def __str__(self):
        return self.name

class VolunteerHistory(models.Model):
    volunteer_name = models.CharField(max_length=255, default='Unknown Volunteer')  # Set the default value
    activity = models.ForeignKey(Activity, default=1, on_delete=models.CASCADE)
    date = models.DateField()
    hours = models.PositiveIntegerField()

    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.volunteer_name} - {self.activity.name} ({self.date})"

class VolunteerOpportunity(models.Model):
    CATEGORY_CHOICES = [
        ('environmental', 'Environmental'),
        ('educational', 'Educational'),
        ('community_service', 'Community Service'),
        ('interfaith', 'Interfaith'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    image = models.URLField(null=True, blank=True)
    location = models.CharField(max_length=200)
    age_requirement = models.CharField(max_length=100)
    attendees = models.IntegerField(default=0)
    contact_info = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.title


class SignUp(models.Model):
    opportunity = models.ForeignKey(VolunteerOpportunity, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return f"{self.name} - {self.opportunity.title}"

class PrayerRequest(models.Model):
    prayer_message = models.TextField()
    faith_tradition = models.CharField(max_length=100, blank=True, null=True)
    language = models.CharField(max_length=50, blank=True, null=True)
    is_anonymous = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.prayer_message[:50]  # Return the first 50 characters of the prayer

class Reply(models.Model):
    prayer_request = models.ForeignKey(PrayerRequest, related_name='replies', on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message[:20]  # Return the first 20 characters of the reply message

class CulturalStory(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='stories/', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)  # This field should be defined

    def __str__(self):
        return self.title

class Charity(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    founder_name = models.CharField(max_length=255)
    founder_email = models.EmailField()

    def __str__(self):
        return self.name

class InitiativeJoin(models.Model):
    charity = models.ForeignKey(Charity, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} joined {self.charity.name}'

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.name}'

class Donation(models.Model):
    charity = models.ForeignKey(Charity, related_name='donations', on_delete=models.CASCADE)
    donor_name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Donation of {self.amount} by {self.donor_name} to {self.charity.name}'

class Festival(models.Model):
    name = models.CharField(max_length=100)
    community = models.CharField(max_length=100)
    date = models.DateField()
    icon = models.URLField()

    def __str__(self):
        return f"{self.name} ({self.community})"
