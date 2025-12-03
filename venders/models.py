from django.db import models
from banks.models import Bank

class Vendor(models.Model):
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, related_name="vendors")
    company_name = models.CharField(max_length=255)
    email = models.EmailField()
    category = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['bank', 'email']),
        ]
    def __str__(self):
        return self.company_name