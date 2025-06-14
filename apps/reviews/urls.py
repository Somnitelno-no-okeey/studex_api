from django.urls import path
from .views import (
    ReviewCreateView,
    ReviewListView,
    ReviewDetailView,
    ReviewUpdateView,
    ReviewDeleteView,
)

urlpatterns = [
    # POST — создание отзыва
    path('<uuid:discipline_id>/', ReviewCreateView.as_view(), name='create-review'),

    # GET — список отзывов по дисциплине
    path('disciplines/<uuid:discipline_id>/', ReviewListView.as_view(), name='review-list'),

    # GET — один отзыв (например, для редактирования)
    path('<uuid:pk>/', ReviewDetailView.as_view(), name='review-detail'),

    # PATCH/PUT — обновление
    path('<uuid:pk>/update/', ReviewUpdateView.as_view(), name='update-review'),

    # DELETE — удаление
    path('<uuid:pk>/', ReviewDeleteView.as_view(), name='delete-review'),
]
