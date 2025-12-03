from rest_framework import viewsets
from .models import Bank
from .serializers import BankSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class BankViewSet(viewsets.ModelViewSet):
    queryset = Bank.objects.all()
    serializer_class = BankSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]