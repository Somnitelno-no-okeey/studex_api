from django.urls import path
from .views import DisciplineListAPIView, DisciplineDetailAPIView, ModuleListAPIView

urlpatterns = [
    path('', DisciplineListAPIView.as_view(), name='discipline-list'),
    path('<uuid:id>/', DisciplineDetailAPIView.as_view(), name='discipline-detail'),
    path('modules/', ModuleListAPIView.as_view(), name= 'modules-list'),
]
