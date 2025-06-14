from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Review
from .serializers import ReviewSerializer, ReviewListSerializer
from apps.disciplines.models import Discipline


class ReviewCreateListView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ReviewSerializer
        return ReviewListSerializer
    
    def get_queryset(self):
        return Review.objects.filter(discipline_id=self.kwargs['discipline_id'])
    
    def perform_create(self, serializer):
        discipline = Discipline.objects.get(pk=self.kwargs['discipline_id'])
        serializer.save(user=self.request.user, discipline=discipline)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['discipline'] = Discipline.objects.get(pk=self.kwargs['discipline_id'])
        context['request'] = self.request
        return context


class ReviewDetailView(generics.RetrieveAPIView):
    serializer_class = ReviewListSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'
    
    def get_queryset(self):
        return Review.objects.filter(user=self.request.user, discipline_id=self.kwargs['discipline_id'])


class ReviewUpdateView(generics.UpdateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'
    
    def get_queryset(self):
        return Review.objects.filter(user=self.request.user, discipline_id=self.kwargs['discipline_id'])
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['discipline'] = Discipline.objects.get(pk=self.kwargs['discipline_id'])
        context['request'] = self.request
        return context
    
    def get_object(self):
        obj = super().get_object()
        if obj.user != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied("Вы не можете редактировать чужой отзыв.")
        return obj


class ReviewDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'
    
    def get_queryset(self):
        return Review.objects.filter(user=self.request.user, discipline_id=self.kwargs['discipline_id'])
    
    def get_object(self):
        obj = super().get_object()
        if obj.user != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied("Вы не можете удалить чужой отзыв.")
        return obj