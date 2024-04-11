from django.test import TestCase, Client
# Create your tests here.


class test(TestCase):

    def test_response(self):
        c = Client()
        response = c.get(("create-listing/"))
        self.assertEqual(response.status_code, 400)
