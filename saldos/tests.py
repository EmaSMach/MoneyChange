from django.test import TestCase
from django.urls import reverse


# Create your tests here.


class ATMViewTestCase(TestCase):
    def setUp(self):
        self.operations_url = "operations" # lo que ponesmos en la url cuando decimos name="product_detail", por ej

    def test_post(self):
        data = {
            "amount": 500
        }
        test_id = 45

        response = self.client.get(reverse(self.operations_url, kwargs={"account_id": test_id}), data=data)

        expected_response = {"error": {"message": f"Account with ID {test_id} not found."}}

        self.assertEqual(expected_response, response.json()) # checkeamos que sean iguales
        # hay un buen número de estos "asserts"
