# events/admin.py

from django.contrib import admin
from .models import Community, Thread, Comment, VolunteerOpportunity, CulturalStory, Charity, Contact, Donation


@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'is_interfaith')  # Fields to display
    search_fields = ('name', 'created_by__username')  # Fields to search in the admin interface

admin.site.register(Thread)
admin.site.register(Comment)
admin.site.register(VolunteerOpportunity)
admin.site.register(Charity)
admin.site.register(Contact)
admin.site.register(Donation)


@admin.register(CulturalStory)
class CulturalStoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_approved', 'created_at')
    list_filter = ('is_approved',)
    search_fields = ('title', 'description')

    # Add an action to approve stories in bulk
    actions = ['approve_stories']

    def approve_stories(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, "Selected stories have been approved.")
    approve_stories.short_description = "Approve selected stories"

