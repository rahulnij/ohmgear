from rest_framework.test import APITestCase, APIClient
import unittest


class StaticPagesTestCase(APITestCase):
    client = APIClient()

    fixtures = ['default']

    def test_create(self):
        response = self.client.post('/api/staticpages/',
                                    {"page_name": "test",
                                     "content": "this is test page",
                                     "headline": "test headline",
                                     "status": "1",
                                     "detail": "test"},
                                    format='json')
        self.assertEqual(response.status_code, 200)

    @unittest.skip("Error in Test")
    def test_list_static_pages(self):
        response = self.client.post('/api/staticpages/',
                                    {"page_name": "test",
                                     "content": "this is test page",
                                     "headline": "test headline",
                                     "status": "1",
                                     "detail": "test"},
                                    format='json')
        """ get static page """
        response = self.client.get(
            '/api/staticpages/', {"page_name": "test"}, format='json')
        self.assertEqual(response.status_code, 200)
