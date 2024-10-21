from django.urls import path
from events.views import (
    index,  # Changed 'home' to 'index'
    register,
    user_login,
    user_logout,
    community_list_view,
    community_details_view,
    community_create_view,
    event_list_view,
    event_details_view,
    event_create_view,
    interfaith_networking,
    CustomLoginView,
    about_us,
    contact,
    OfferHelpView,
    RequestHelpView,
    OfferHelpCategoryView,
    RequestHelpCategory1View,
    RequestHelpCategory2View,
    RequestHelpCategory3View,
    RequestHelpCategory4View,
    community_networking,
    search_users,
    create_poll,
    respond_to_poll,
    send_connection_request,
    discussion_forums,
    create_thread,
    add_comment,
    request_resource,
    profile_edit,
    notification_center,
    mark_as_read,
    delete_notification,
    settings_view,
    delete_request_view,
    edit_request_view,
    create_community_profile,
    view_thread, volunteer_opportunities, sign_up, profile_view,
    add_activity,
    resource_list,
    add_resource,
    enable_2fa,
    update_profile_picture, 
    update_personal_info,
    shared_prayer_requests,
    submit_prayer, 
    prayer_feed,
    submit_reply, gamification_elements_view, share_culture, list_cultural_stories, thank_you, admin_approve_story,
    charitable_initiatives, add_charity,
)



urlpatterns = [
    path('', index, name='index'),  # Changed 'home' to 'index'
    path('register/', register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),  # Keep the login path here
    path('logout/', user_logout, name='logout'),
    path('communities/', community_list_view, name='community_list'),
    path('communities/<int:community_id>/', community_details_view, name='community_details'),
    path('communities/create/', community_create_view, name='community_create'),
    path('create-community/', create_community_profile, name='community_form'),
    path('events/', event_list_view, name='event_list'),
    path('events/<int:event_id>/', event_details_view, name='event_details'),
    path('events/create/', event_create_view, name='event_create'),
    path('interfaith_networking/', interfaith_networking, name='interfaith_networking'),
    path('about/', about_us, name='about_us'),
    path('contact/', contact, name='contact'),
    path('offer_help/', OfferHelpView.as_view(), name='offer_help'),
    path('request_help/', RequestHelpView.as_view(), name='request_help'),
    path('offer_help_category_1/', OfferHelpCategoryView.as_view(), {'category': 'Mental Health Support'}, name='offer_help_category_1'),
    path('offer-help/category-2/', OfferHelpCategoryView.as_view(), {'category': 'Food Assistance'}, name='offer_help_category_2'),
    path('offer-help/category-3/', OfferHelpCategoryView.as_view(), {'category': 'Shelter Services'}, name='offer_help_category_3'),
    path('offer-help/category-4/', OfferHelpCategoryView.as_view(), {'category': 'Educational Support'}, name='offer_help_category_4'),
    path('offer_help/submit/', OfferHelpView.as_view(), name='offer_help_submit'),
    path('request_help_category_1/', RequestHelpCategory1View.as_view(), name='request_help_category_1'),
    path('request-help/category-2/', RequestHelpCategory2View.as_view(), name='request_help_category_2'),
    path('request-help/category-3/', RequestHelpCategory3View.as_view(), name='request_help_category_3'),
    path('request-help/category-4/', RequestHelpCategory4View.as_view(), name='request_help_category_4'),
    path('request_help/submit/', RequestHelpView.as_view(), name='request_help_submit'),
    path('community/', community_networking, name='community_networking'),
    path('search/', search_users, name='search_users'),
    path('poll/create/', create_poll, name='create_poll'),
    path('poll/respond/<int:poll_id>/', respond_to_poll, name='respond_to_poll'),
    path('connect/<int:user_id>/', send_connection_request, name='send_connection_request'),
    path('forums/', discussion_forums, name='discussion_forums'),
    path('forums/create_thread/', create_thread, name='create_thread'),
    path('forums/add_comment/', add_comment, name='add_comment'),
    path('forums/request_resource/', request_resource, name='request_resource'),
    path('profile/edit/', profile_edit, name='profile_edit'),
    path('notifications/', notification_center, name='notification_center'),
    path('notifications/mark_as_read/<int:notification_id>/', mark_as_read, name='mark_as_read'),
    path('notifications/delete/<int:notification_id>/', delete_notification, name='delete_notification'),
    path('settings/', settings_view, name='settings'),
    path('delete_request/<int:request_id>/', delete_request_view, name='delete_request'),
    path('edit_request/<int:request_id>/', edit_request_view, name='edit_request'),
    path('thread/<int:thread_id>/', view_thread, name='view_thread'),
    path('create-thread/', create_thread, name='create_thread'),
    path('events/thread/<int:thread_id>/', view_thread, name='view_thread'),
    path('events/thread/<int:thread_id>/add_comment/', add_comment, name='add_comment'),
    path('volunteer-opportunities/', volunteer_opportunities, name='volunteer_opportunities'),
    path('sign-up/<int:opportunity_id>/', sign_up, name='sign_up'),  # Sign-up page for a specific opportunity
    path('profile/', profile_view, name='profile_view'),  # View user profile
    path('activity/add/', add_activity, name='add_activity'),  # Add an activity
    path('resources/', resource_list, name='resource_list'),  # List resources
    path('resources/add/', add_resource, name='add_resource'),  # Add a resource
    path('2fa/enable/', enable_2fa, name='enable_2fa'),  # Enable two-factor authentication
    path('profile/update/picture/', update_profile_picture, name='update_profile_picture'),
    path('profile/update/info/', update_personal_info, name='update_personal_info'),
    path('profile/', profile_view, name='profile'),  # Ensure this line is present
    path('api/submit-prayer/', submit_prayer, name='submit_prayer'),  # API endpoint for submitting prayers
    path('api/get-prayers/', prayer_feed, name='prayer_feed'),  # API endpoint for retrieving prayers
    path('shared-prayer-requests/', shared_prayer_requests, name='shared_prayer_requests'),
    path('api/submit-reply/', submit_reply, name='submit_reply'),  # New endpoint
    path('gamification/', gamification_elements_view, name='gamification_elements'),
    path('share_culture', share_culture, name='cultural_exchange'),
    path('thank-you/', thank_you, name='thank_you'),
    path('stories/', list_cultural_stories, name='list_stories'),
    
    # Admin URLs for approving stories
    path('admin/approve/<int:story_id>/', admin_approve_story, name='admin_approve_story'),
    path('charitable_initiatives/<int:user_id>/', charitable_initiatives, name='charitable_initiatives'),
    path('add-charity/', add_charity, name='add_charity'),


]
