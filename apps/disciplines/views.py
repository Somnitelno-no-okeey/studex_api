from drf_spectacular.utils import extend_schema
from rest_framework import generics

from apps.disciplines.models import Discipline
from apps.disciplines.serializers import (
    DisciplineListSerializer,
    DisciplineDetailSerializer,
    DisciplineCreateUpdateSerializer,
)
from apps.disciplines.models import Module
from apps.disciplines.serializers import ModuleSerializer


@extend_schema(tags=['Disciplines'])
class DisciplineListAPIView(generics.ListAPIView):
    queryset = Discipline.objects.all()
    serializer_class = DisciplineListSerializer


@extend_schema(tags=['Disciplines'])
class DisciplineDetailAPIView(generics.RetrieveAPIView):
    queryset = Discipline.objects.all()
    serializer_class = DisciplineDetailSerializer
    lookup_field = 'id'


@extend_schema(tags=['Disciplines'])
class DisciplineCreateAPIView(generics.CreateAPIView):
    queryset = Discipline.objects.all()
    serializer_class = DisciplineCreateUpdateSerializer

@extend_schema(tags=['Modules'])
class ModuleListAPIView(generics.ListAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    pagination_class = None