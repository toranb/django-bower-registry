import json
from api.models import Package
from django.test import TestCase
from south.migration import Migrations
from django.db.utils import OperationalError
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

    def test_returns_package_when_name_includes_hyphen(self):
        Package.objects.create(name="ember-data", url="/foo")
        url = reverse("find", kwargs={'name': 'ember-data'})
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        result = json.loads(response.content)
        self.assertEqual(result['url'], '/foo')
        self.assertEqual(result['name'], 'ember-data')

    def test_returns_package_when_name_includes_period(self):
        Package.objects.create(name="backbone.wreqr", url="/foo")
        url = reverse("find", kwargs={'name': 'backbone.wreqr'})
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        result = json.loads(response.content)
        self.assertEqual(result['name'], 'backbone.wreqr')

    def test_can_update_package(self):
        Package.objects.create(name="ember", url="/foo")
        url = reverse("find", kwargs={'name': 'ember'})
        response = self.client.put(url, {'url': '/bar', 'name': 'ember'}, 'application/json', content_type=MULTIPART_CONTENT)
        self.assertEqual(200, response.status_code)
        result = json.loads(response.content)
        self.assertEqual(result['url'], '/bar')
        self.assertEqual(result['name'], 'ember')


class PackagesSearchViewTests(TestCase):

    def test_returns_list_of_packages_when_search_finds_match(self):
        Package.objects.create(name="ember", url="/foo")
        url = reverse("search", kwargs={'name': 'mbe'})
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        results = json.loads(response.content)
        self.assertEqual(1, len(results))
        self.assertEqual(results[0]['url'], '/foo')
        self.assertEqual(results[0]['name'], 'ember')

    def test_returns_empty_list_when_search_finds_no_match(self):
        Package.objects.create(name="ember", url="/foo")
        url = reverse("search", kwargs={'name': 'wat'})
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(b'[]', response.content)

    def test_returns_list_of_packages_when_name_includes_hyphen(self):
        Package.objects.create(name="ember-data", url="/foo")
        url = reverse("search", kwargs={'name': 'ember-da'})
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        results = json.loads(response.content)
        self.assertEqual(1, len(results))
        self.assertEqual(results[0]['url'], '/foo')
        self.assertEqual(results[0]['name'], 'ember-data')

    def test_returns_list_of_packages_when_name_includes_period(self):
        Package.objects.create(name="backbone.wreqr", url="/foo")
        url = reverse("search", kwargs={'name': 'backbone.wre'})
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        results = json.loads(response.content)
        self.assertEqual(1, len(results))
        self.assertEqual(results[0]['url'], '/foo')
        self.assertEqual(results[0]['name'], 'backbone.wreqr')


class TestORM(object):

    def __init__(self):
        self.Package =  Package


class MigrationsTests(TestCase):

    def setUp(self):
        self.sut = self._pick_migration('0001_initial')

    def test_forward_and_backwards_migrations_work(self):
        self.sut.migration_instance().backwards(TestORM())
        self.assertTableDoesNotExist()

        self.sut.migration_instance().forwards(TestORM())
        self.assertEqual([], list(Package.objects.all()))

        self.sut.migration_instance().backwards(TestORM())
        self.assertTableDoesNotExist()

    def assertTableDoesNotExist(self):
        with self.assertRaises(OperationalError) as c:
            list(Package.objects.all())
        self.assertEqual("no such table: api_package", c.exception.args[0])

    def _pick_migration(self, name):
        migrations = Migrations('api')
        for migration in migrations:
            if migration.full_name().split(".")[-1] == name:
                return migration
