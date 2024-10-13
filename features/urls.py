from django.urls import path
from . import views

urlpatterns = [
    path('', views.feature_list, name='feature_list'),
    path('<int:feature_id>/', views.feature_detail, name='feature_detail'),
]
