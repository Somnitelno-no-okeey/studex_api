from django.urls import path
from .views import (
    ReviewCreateListView,
    ReviewDetailView,
    ReviewUpdateView,
    ReviewDeleteView,
    UserReviewView,
)

urlpatterns = [
    path('<uuid:discipline_id>/reviews/', ReviewCreateListView.as_view(), name='review-list-create'),

    path('<uuid:discipline_id>/reviews/<uuid:pk>/', ReviewDetailView.as_view(), name='review-detail'),
    
    path('<uuid:discipline_id>/reviews/<uuid:pk>/update/', ReviewUpdateView.as_view(), name='update-review'),
    
    path('<uuid:discipline_id>/reviews/<uuid:pk>/delete/', ReviewDeleteView.as_view(), name='delete-review'),
    
    path('<uuid:discipline_id>/user_review/', UserReviewView.as_view(), name='user-review'),
]