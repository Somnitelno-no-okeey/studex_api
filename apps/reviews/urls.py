from django.urls import path
from apps.reviews.views import ReviewListAPIView

urlpatterns = [
    path('review-list/', ReviewListAPIView.as_view(), name='review-list'),
]
