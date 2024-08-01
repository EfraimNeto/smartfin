from django.test import TestCase
from django.urls import reverse

class DashboardURLTest(TestCase):
    def test_deshboard_url_is_correct(self):
        url = reverse('home')
        self.assertEqual(url, '/')

    def test_login_url_is_correct(self):
        url = reverse('login')
        self.assertEqual(url, '/login/')

    def test_logout_url_is_correct(self):
        url = reverse ('logout')
        self.assertEqual(url, '/logout/')