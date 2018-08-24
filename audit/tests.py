from django.test import TestCase

# Create your tests here.
from django.core.urlresolvers import reverse
from django.urls import resolve
from django.test import TestCase
from .views import acc_login


class HomeTests(TestCase):
    def test_home_view_status_code(self):
        url = reverse('login')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve('login')
        self.assertEquals(view.func, acc_login)

