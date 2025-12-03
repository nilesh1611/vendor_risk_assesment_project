from rest_framework import serializers
from .models import Question

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id','bank','category','question_text','question_type','validation_rules','risk_weight','version','is_active']
        read_only_fields = ['id','created_at']