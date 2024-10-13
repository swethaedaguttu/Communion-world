from django.shortcuts import render, get_object_or_404, redirect
from .models import Feature, Feedback
from .forms import FeedbackForm
from django.contrib import messages

# View to list all features
def feature_list(request):
    features = Feature.objects.all()  # Retrieve all features from the database
    return render(request, 'features/feature_list.html', {'features': features})

# View to display details for a specific feature
def feature_detail(request, feature_id):
    feature = get_object_or_404(Feature, id=feature_id)  # Get feature by ID or return 404
    return render(request, 'features/feature_detail.html', {'feature': feature})

# View to handle feedback submission
def submit_feedback(request, feature_id):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)  # Create a form instance with submitted data
        if form.is_valid():
            feedback = form.save(commit=False)  # Create a Feedback instance but don’t save yet
            feedback.feature_id = feature_id  # Set the related feature
            feedback.save()  # Save feedback to the database
            messages.success(request, 'Thank you for your feedback!')  # Show success message
            return redirect('feature_detail', feature_id=feature_id)  # Redirect to feature detail page
    else:
        form = FeedbackForm()  # Create a new form instance
    return render(request, 'features/feature_detail.html', {'form': form})

