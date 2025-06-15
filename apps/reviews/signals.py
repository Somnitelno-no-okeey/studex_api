from django.dispatch import receiver
from django.db.models.signals import pre_save
from .models import Review

@receiver(pre_save, sender=Review)
def calculate_average_on_pre_save(sender, instance, **kwargs):
    scores = []
    if instance.is_interest_active:
        scores.append(instance.interest)
    if instance.is_complexity_active:
        scores.append(instance.complexity)
    if instance.is_usefulness_active:
        scores.append(instance.usefulness)
    if instance.is_workload_active:
        scores.append(instance.workload)
    if instance.is_logical_structure_active:
        scores.append(instance.logical_structure)
    if instance.is_practical_applicability_active:
        scores.append(instance.practical_applicability)
    if instance.is_teaching_effectiveness_active:
        scores.append(instance.teaching_effectiveness)
    if instance.is_materials_availability_active:
        scores.append(instance.materials_availability)
    if instance.is_feedback_support_active:
        scores.append(instance.feedback_support)
    
    if scores:
        instance.avg_rating = sum(scores) / len(scores) 
    else:
        instance.avg_rating = 0