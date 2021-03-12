from django.test import TestCase, Client
from .models import Solder, Exhibit

class SoldertestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.csrf_client = Client(enforce_csrf_checks=True)

    def test_solder_list(self):
        