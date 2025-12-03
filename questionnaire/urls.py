from django.urls import path
from .views import BankQuestionnaireAPIView

urlpatterns = [
    path("<int:bank_id>/", BankQuestionnaireAPIView.as_view(), name="bank-questionnaire"),
]