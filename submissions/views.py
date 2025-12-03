from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .serializers import SubmissionSerializer
from .models import Submission
from django.shortcuts import get_object_or_404

class SubmissionCreateAPIView(generics.CreateAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.AllowAny]

class BankSubmissionsListAPIView(generics.ListAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        bank_id = self.kwargs.get('bank_id')
        return Submission.objects.filter(bank_id=bank_id).select_related('vendor','bank').prefetch_related('answers')

class UpdateRiskRatingAPIView(generics.UpdateAPIView):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.AllowAny]

    def put(self, request, *args, **kwargs):
        submission = get_object_or_404(Submission, pk=kwargs.get('pk'))
        final = request.data.get('final_risk_score')
        if final is not None:
            submission.final_risk_score = final
            submission.status = 'COMPLETED'
            submission.save()
            return Response({"detail":"Risk rating updated."})
        return Response({"detail":"final_risk_score required."}, status=status.HTTP_400_BAD_REQUEST)