from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from vendors.models import Vendor, Bank
from django.contrib.auth.models import User
import json


class VendorRegistrationTest(TestCase):
    def setUp(self):
        self.bank = Bank.objects.create(name="Bank A")

        # Create a superuser to simulate admin (if needed)
        self.user = User.objects.create_user(username="admin", password="password123")

        # Initialize DRF API client
        self.client = APIClient()
        # Authenticate user if endpoint requires auth
        self.client.force_authenticate(user=self.user)
        self.valid_payload = {
            "company_name": "ACME Corp",
            "email": "contact@acme.com",
            "bank_id": self.bank.id,
            "category": "Software"
        }
        self.invalid_payload = {
            "company_name": "Fake Vendor",
            "email": "fakeemail@gmail.com",  # non-corporate email
            "bank_id": self.bank.id,
            "category": "Software"
        }

    def test_vendor_registration_success(self):
        response = self.client.post("/api/vendors/register/", self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vendor.objects.count(), 1)
        vendor = Vendor.objects.first()
        self.assertEqual(vendor.company_name, self.valid_payload["company_name"])
        self.assertEqual(vendor.bank, self.bank)

    def test_vendor_registration_invalid_email(self):
        response = self.client.post("/api/vendors/register/", self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)
        self.assertEqual(Vendor.objects.count(), 0)

    def test_vendor_registration_missing_field(self):
        payload = self.valid_payload.copy()
        payload.pop("company_name")
        response = self.client.post("/api/vendors/register/", payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("company_name", response.data)
        self.assertEqual(Vendor.objects.count(), 0)

    def test_vendor_registration_duplicate_email(self):
        """Test that duplicate email registration is not allowed"""
        self.client.post("/api/vendors/register/", self.valid_payload, format='json')
        response = self.client.post("/api/vendors/register/", self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Vendor.objects.count(), 1)
