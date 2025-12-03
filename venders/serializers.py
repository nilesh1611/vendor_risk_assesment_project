from rest_framework import serializers
from .models import Vendor
import re

class VendorRegistrationSerializer(serializers.ModelSerializer):
    bank_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Vendor
        fields = ['id', 'bank_id', 'company_name', 'email', 'category', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_email(self, value):
        # corporate email validation: simple domain check
        allowed_domains = ['company.com']
        domain = value.split('@')[-1]
        if domain not in allowed_domains:
            raise serializers.ValidationError("Corporate email domain not allowed.")
        return value

    def create(self, validated_data):
        bank_id = validated_data.pop('bank_id')
        from banks.models import Bank
        bank = Bank.objects.get(pk=bank_id)
        vendor = Vendor.objects.create(bank=bank, **validated_data)
        return vendor