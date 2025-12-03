import pytest
from tests.factories import BankFactory

@pytest.mark.django_db
def test_vendor_registration(client):
    bank = BankFactory()

    body = {
        "bank_id": bank.id,
        "company_name": "Acme Ltd",
        "email": "user@acme.com",
        "category": "IT"
    }

    res = client.post("/api/vendors/register/", body, format="json")

    assert res.status_code == 201
    assert res.json()["bank"] == bank.id
    assert res.json()["company_name"] == "Acme Ltd"
