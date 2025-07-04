from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView
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
        queryset = Review.objects.filter(discipline_id=self.kwargs['discipline_id'])
        
        sort_by = self.request.query_params.get('sort_by', None)
        order = self.request.query_params.get('order', None) 
        
        valid_sort_fields = ['rating', 'date']
        
        if sort_by in valid_sort_fields:
            if sort_by == 'rating':
                order_field = 'avg_rating'
            elif sort_by == 'date':
                order_field = 'created_at'
            
            if order.lower() == 'desc':
                order_field = f'-{order_field}'
            
            queryset = queryset.order_by(order_field)
        
        return queryset
   
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
    http_method_names = ['put', 'options']
   
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


class UserReviewView(APIView):
    permission_classes = [permissions.IsAuthenticated]
   
    def get(self, request, discipline_id):
        try:
            review = Review.objects.filter(user=request.user, discipline_id=discipline_id).first()
            return Response({"review_id": review.pk if review else None})
        except Review.DoesNotExist:
            return Response({"review_id": None})