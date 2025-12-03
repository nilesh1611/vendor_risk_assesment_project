from django.db import models
from banks.models import Bank

class Question(models.Model):
    QUESTION_TYPES = [('TEXT','text'),('MCQ','mcq'),('NUM','number'),('BOOL','bool')]
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, related_name="questions")
    category = models.CharField(max_length=100)
    question_text = models.TextField()
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES)
    validation_rules = models.JSONField(default=dict)
    risk_weight = models.PositiveSmallIntegerField(default=1)
    version = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['bank','category','version'])
        ]
    def __str__(self):
        return f"{self.category} - v{self.version}"