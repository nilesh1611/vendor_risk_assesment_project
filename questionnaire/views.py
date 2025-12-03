from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Question
from .serializers import QuestionSerializer
from django.core.cache import cache

class BankQuestionnaireAPIView(APIView):
    def get(self, request, bank_id):
        category = request.query_params.get('category')
        cache_key = f"questionnaire:{bank_id}:{category}"
        data = cache.get(cache_key)
        if data:
            return Response(data)
        qs = Question.objects.filter(bank_id=bank_id, is_active=True)
        if category:
            qs = qs.filter(category=category)
        qs = qs.order_by('-version')
        serializer = QuestionSerializer(qs, many=True)
        cache.set(cache_key, serializer.data, 3600)
        return Response(serializer.data, status=status.HTTP_200_OK)