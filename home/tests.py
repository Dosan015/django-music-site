from django.test import TestCase

from django.test import Client
from django.urls import reverse

class PageViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home(self):
        resp = self.client.get(reverse('home'))
        self.assertEqual(
            resp.status_code, 200
        )
