from rest_framework import generics, permissions
from .models import Review
from .serializers import ReviewSerializer, ReviewListSerializer
from apps.disciplines.models import Discipline


class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        discipline = Discipline.objects.get(pk=self.kwargs['discipline_id'])
        serializer.save(user=self.request.user, discipline=discipline)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['discipline'] = Discipline.objects.get(pk=self.kwargs['discipline_id'])
        return context


class ReviewListView(generics.ListAPIView):
    serializer_class = ReviewListSerializer

    def get_queryset(self):
        return Review.objects.filter(discipline_id=self.kwargs['discipline_id'])


class ReviewDetailView(generics.RetrieveAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)


class ReviewUpdateView(generics.UpdateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)
    
    def get_object(self):
        obj = super().get_object()
        if obj.user != self.request.user:
            raise PermissionDenied("Вы не можете редактировать чужой отзыв.")
        return obj


class ReviewDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)

    def get_object(self):
        obj = super().get_object()
        if obj.user != self.request.user:
            raise PermissionDenied("Вы не можете удалить чужой отзыв.")
        return obj