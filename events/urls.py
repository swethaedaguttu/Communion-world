from django.urls import path
from events.views import (
    index,
    register,
    login_view,
    user_logout,
    event_list_view,
    event_create_view,
    event_details_view,
    join_event,
    CustomLoginView,
    about_us,
    contact,
    help_alert,
    profile_view,
    profile_edit,
    submit_help_alert,
    notification_center,
    mark_as_read,
    delete_notification,
    settings_view,
    update_profile_picture, 
    update_personal_info,
    community_leaders_list,
    create_community_leader,
    community_leader_detail,
    social_issues_groups_list,
    create_social_issues_group,
    group_conversation_detail,
    donation_page, 
    donation_success, 
    donation_list, 
    send_message, 
    help_alert_details,
)

urlpatterns = [
    # Home and registration paths
    path('', index, name='index'),
    path('register/', register, name='register'),
    
    # Login/logout paths
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', user_logout, name='logout'),
    
    # Event management
    path('events/', event_list_view, name='event_list'),
    path('event/<int:event_id>/', event_details_view, name='event_details'),
    path('events/create/', event_create_view, name='event_create'),
    path('event/join/<int:event_id>/', join_event, name='join_event'),
    
    # Information pages
    path('about/', about_us, name='about_us'),
    path('contact/', contact, name='contact'),
    
    # Profile and settings
    path('profile/', profile_view, name='profile'),  # View user profile
    path('profile/edit/', profile_edit, name='profile_edit'),
    path('update_profile_picture/', update_profile_picture, name='update_profile_picture'),
    path('update_personal_info/', update_personal_info, name='update_personal_info'),
    path('settings/', settings_view, name='settings'),
    
    # Notifications
    path('notifications/', notification_center, name='notification_center'),
    path('notifications/mark_as_read/<int:notification_id>/', mark_as_read, name='mark_as_read'),
    path('notifications/delete/<int:notification_id>/', delete_notification, name='delete_notification'),
    
    # Help Alerts
    path('help-alert/', help_alert, name='help_alert'),
    path('submit-help/', submit_help_alert, name='submit_help'),
    path('help-alert/<int:id>/', help_alert_details, name='help_alert_details'),
    
    # Donation paths
    path('donation/request/', donation_page, name='donation_page'),
    path('donation/success/<int:donation_id>/', donation_success, name='donation_success'),
    path('donation/list/', donation_list, name='donation_list'),
    
    # Community Leaders paths
    path('leaders/', community_leaders_list, name='community_leaders_list'),
    path('leaders/create/', create_community_leader, name='create_community_leader'),
    path('leaders/<str:identity_symbol>/', community_leader_detail, name='community_leader_detail'),
    
    # Social Issues Groups paths
    path('groups/', social_issues_groups_list, name='social_issues_groups_list'),
    path('groups/create/', create_social_issues_group, name='create_social_issues_group'),
    path('groups/<int:group_id>/', group_conversation_detail, name='group_conversation_detail'),
    
    # Unified message sending
    path('leaders/<int:leader_id>/send_message/', send_message, name='send_message'),
]
