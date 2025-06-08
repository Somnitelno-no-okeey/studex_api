from django.contrib import admin
from .models import Discipline, Lecturer, Module

@admin.register(Discipline)
class DisciplineAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
      return ["name", "module", "format", "control_type"]

    def get_fields(self, request, obj=None):
      return ["name", "module", "format", "control_type", "description", "teachers"]
    
@admin.register(Lecturer)
class LecturerAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
      return ["first_name", "last_name", "patronymic"]

    def get_fields(self, request, obj=None):
      return ["first_name", "last_name", "patronymic"]


@admin.register(Module)
class LecturerAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
      return ["name"]

    def get_fields(self, request, obj=None):
      return ["name"]
