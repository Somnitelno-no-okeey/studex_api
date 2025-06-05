from django.urls import path
from apps.disciplines.views import DisciplineListAPIView

urlpatterns = [
    path('discipline-list/', DisciplineListAPIView.as_view(), name='discipline-list'),
]
