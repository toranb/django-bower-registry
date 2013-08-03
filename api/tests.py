import json
from api.models import Package
from django.test import TestCase
from django.core.urlresolvers import reverse


class PackagesListViewTests(TestCase):

    def test_returns_list_of_packages(self):
        Package.objects.create(name="ember", url="/foo")
        Package.objects.create(name="moment", url="/bar")
        url = reverse("list")
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        results = json.loads(response.content)
        self.assertEqual(2, len(results))
        self.assertEqual(results[0]['url'], '/foo')
        self.assertEqual(results[0]['name'], 'ember')
        self.assertEqual(results[1]['url'], '/bar')
        self.assertEqual(results[1]['name'], 'moment')

class PackagesFindViewTests(TestCase):

    def test_returns_package_by_name(self):
        Package.objects.create(name="ember", url="/foo")
        url = reverse("find", kwargs={'name': 'ember'})
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        result = json.loads(response.content)
        self.assertEqual(result['url'], '/foo')
        self.assertEqual(result['name'], 'ember')

    def test_returns_404_when_package_name_not_found(self):
        Package.objects.create(name="ember", url="/foo")
        url = reverse("find", kwargs={'name': 'wat'})
        response = self.client.get(url)
        self.assertEqual(404, response.status_code)
