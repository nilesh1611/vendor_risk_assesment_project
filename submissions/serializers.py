from rest_framework import serializers
from .models import Submission, Answer, RiskScore
from questionnaire.models import Question

class AnswerSerializer(serializers.ModelSerializer):
    question_id = serializers.IntegerField()
    class Meta:
        model = Answer
        fields = ['id','question_id','answer_value','question_version']

class SubmissionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)
    bank_id = serializers.IntegerField(write_only=True)
    vendor_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Submission
        fields = ['id','vendor_id','bank_id','status','submitted_at','version','inherent_risk_score','final_risk_score','answers']
        read_only_fields = ['id','submitted_at','inherent_risk_score','final_risk_score']

    def validate(self, data):
        # Basic validation: must have answers if submitting
        if data.get('status') == 'SUBMITTED' and not data.get('answers'):
            raise serializers.ValidationError("Answers required for submission.")
        return data

    def create(self, validated_data):
        answers_data = validated_data.pop('answers', [])
        bank_id = validated_data.pop('bank_id')
        vendor_id = validated_data.pop('vendor_id')
        submission = Submission.objects.create(bank_id=bank_id, vendor_id=vendor_id, **validated_data)
        total_weight = 0
        weighted_sum = 0
        for a in answers_data:
            q = Question.objects.get(pk=a['question_id'])
            Answer.objects.create(submission=submission, question=q, answer_value=a['answer_value'], question_version=q.version)
            # assume answer_value is numeric 1-5 for scoring
            try:
                score = float(a['answer_value'])
            except:
                score = 1.0
            weighted_sum += score * q.risk_weight
            total_weight += q.risk_weight
        if total_weight > 0:
            inherent = weighted_sum / total_weight
        else:
            inherent = 0.0
        submission.inherent_risk_score = inherent
        submission.save()
        RiskScore.objects.create(submission=submission, inherent_score=inherent)
        return submission