from django.db import models
from apps.accounts.models import User
from django.contrib.auth import get_user_model
from apps.disciplines.models import Discipline


User = get_user_model()

class Review(models.Model):
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    interest = models.PositiveSmallIntegerField(default=0)
    complexity = models.PositiveSmallIntegerField(default=0)

    usefulness = models.PositiveSmallIntegerField(default=0)
    workload = models.PositiveSmallIntegerField(default=0)
    logical_structure = models.PositiveSmallIntegerField(default=0)
    practical_applicability = models.PositiveSmallIntegerField(default=0)
    teaching_effectiveness = models.PositiveSmallIntegerField(default=0)
    materials_availability = models.PositiveSmallIntegerField(default=0)
    feedback_support = models.PositiveSmallIntegerField(default=0)

    comment = models.TextField(blank=True)
    anonymous = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user} on {self.discipline}"