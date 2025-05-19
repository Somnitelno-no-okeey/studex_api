from rest_framework.views import APIView
from rest_framework.response import Response
from apps.disciplines.models import Discipline
from apps.disciplines.serializers import DisciplineSerializer
from drf_spectacular.utils import extend_schema

class DisciplineListAPIView(APIView):
    @extend_schema(
        responses=DisciplineSerializer(many=True),
        description="Получить список всех дисциплин с преподавателями"
    )
    def get(self, request):
        disciplines = Discipline.objects.all().prefetch_related('lecturers')
        serializer = DisciplineSerializer(disciplines, many=True)
        return Response(serializer.data)