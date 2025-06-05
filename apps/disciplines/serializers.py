from rest_framework import serializers
from .models import Discipline, Lecturer

class LecturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecturer
        fields = ['first_name', 'last_name', 'patronymic']

class DisciplineSerializer(serializers.ModelSerializer):
    lecturers = LecturerSerializer(many=True, read_only=True)
    
    class Meta:
        model = Discipline
        fields = '__all__'  # Или перечислите конкретные поля, которые хотите включать