from rest_framework.views import APIView
from rest_framework.response import Response
from apps.reviews.models import Review
from apps.reviews.serializers import ReviewListSerializer
from drf_spectacular.utils import extend_schema

class ReviewListAPIView(APIView):
    @extend_schema(
        responses=ReviewListSerializer(many=True),
        description="Получить список всех отзывов"
    )
    def get(self, request):
        reviews = Review.objects.all().select_related('user', 'discipline')
        serializer = ReviewListSerializer(reviews, many=True)
        return Response(serializer.data)
