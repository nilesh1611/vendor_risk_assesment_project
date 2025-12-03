from django.db import models
from vendors.models import Vendor
from banks.models import Bank
from questionnaire.models import Question

class Submission(models.Model):
    STATUS_CHOICES = [('DRAFT','DRAFT'),('SUBMITTED','SUBMITTED'),('UNDER_REVIEW','UNDER_REVIEW'),('COMPLETED','COMPLETED')]
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="submissions")
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, related_name="submissions")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    submitted_at = models.DateTimeField(null=True, blank=True)
    version = models.PositiveIntegerField(default=1)
    inherent_risk_score = models.FloatField(null=True, blank=True)
    final_risk_score = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Answer(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(Question, on_delete=models.PROTECT)
    answer_value = models.JSONField()
    question_version = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

class RiskScore(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name="risk_scores")
    inherent_score = models.FloatField()
    final_score = models.FloatField(null=True, blank=True)
    trend = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)