from drf_spectacular.utils import extend_schema
from rest_framework import generics
from django.db.models import Q
from apps.disciplines.models import Discipline, Module, DisciplineFormat, ControlType
from apps.disciplines.serializers import (
    DisciplineListSerializer,
    DisciplineDetailSerializer,
    DisciplineCreateUpdateSerializer,
    ModuleSerializer,
)


@extend_schema(tags=['Disciplines'])
class DisciplineListAPIView(generics.ListAPIView):
    serializer_class = DisciplineListSerializer
    
    def get_queryset(self):
        queryset = Discipline.objects.all()

        sort_by = self.request.query_params.get('sort_by', None)
        order = self.request.query_params.get('order', 'asc')
        rating = self.request.query_params.get('rating', None)
        module = self.request.query_params.get('module', None)
        control_type = self.request.query_params.get('control_type', None)
        discipline_format = self.request.query_params.get('discipline_format', None)
        search = self.request.query_params.get('search', None)

        if rating:
            try:
                rating_value = float(rating)
                if 1 <= rating_value <= 5:
                    queryset = queryset.filter(avg_rating__gte=rating_value)
            except (ValueError, TypeError):
                pass
        if module:
            queryset = queryset.filter(module_id=module)
        
        if control_type:
            control_type_mapping = {
                'exam': 'EXAM',
                'credit': 'CREDIT'
            }
            
            enum_value = control_type_mapping.get(control_type.lower())
            if enum_value:
                queryset = queryset.filter(control_type=enum_value).exclude(control_type__isnull=True).exclude(control_type='')
        
        if discipline_format:
            format_mapping = {
                'online': 'ONLINE',
                'traditional': 'TRADITIONAL',
                'blended': 'BLENDED'
            }
            enum_value = format_mapping.get(discipline_format.lower())
            if enum_value:
                queryset = queryset.filter(format=enum_value).exclude(format__isnull=True).exclude(format='')
        
        if search:
            queryset = queryset.filter(name__icontains=search)
      
        valid_sort_fields = ['rating', 'comment_count']
        if sort_by in valid_sort_fields:
            if sort_by == 'rating':
                order_field = 'avg_rating'
            elif sort_by == 'comment_count':
                order_field = 'review_count'

            if order.lower() == 'desc':
                order_field = f'-{order_field}'
            
            queryset = queryset.order_by(order_field)
        
        return queryset


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