from django.urls import path
from .views import SubmissionCreateAPIView, BankSubmissionsListAPIView, UpdateRiskRatingAPIView

urlpatterns = [
    path("", SubmissionCreateAPIView.as_view(), name="submission-create"),
    path("banks/<int:bank_id>/", BankSubmissionsListAPIView.as_view(), name="bank-submissions"),
    path("<int:pk>/risk-rating/", UpdateRiskRatingAPIView.as_view(), name="update-risk"),
]