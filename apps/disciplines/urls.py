from django.urls import path
from .views import DisciplineListAPIView, DisciplineDetailAPIView

urlpatterns = [
    path('', DisciplineListAPIView.as_view(), name='discipline-list'),
    path('<uuid:id>/', DisciplineDetailAPIView.as_view(), name='discipline-detail'),
]
