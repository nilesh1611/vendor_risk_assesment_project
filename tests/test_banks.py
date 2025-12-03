import pytest
from tests.factories import BankFactory, QuestionFactory

@pytest.mark.django_db
def test_get_bank_questionnaire(client):
    bank = BankFactory()
    q1 = QuestionFactory(bank=bank)

    response = client.get(f"/api/banks/{bank.id}/questionnaire/")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["bank"] == bank.id
