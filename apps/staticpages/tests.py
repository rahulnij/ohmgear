from rest_framework.test import APITestCase, APIClient


class StaticPagesTestCase(APITestCase):
    client = APIClient()

    fixtures = ['default']

    def setUp(self):
        response = self.client.post('/api/staticpages/',
                                    {"page_name": "test",
                                     "content": "this is test page",
                                     "headline": "test headline",
                                     "status": "1",
                                     "detail": "test"},
                                    format='json')
        

    def test_list_static_pages(self):
        """ get static page """
        response = self.client.get(
            '/api/staticpages/', {"page_name": "test"}, format='json')
        self.assertEqual(response.status_code, 200)
