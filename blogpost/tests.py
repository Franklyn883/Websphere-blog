from django.test import TestCase, SimpleTestCase
from django.urls import reverse

class HomePageTest(SimpleTestCase):
    '''Text the home page'''
    def setUp(self):
        url = reverse("home")
        self.response = self.client.get(url)
        
    def test_url_exists_at_correct_location(self):
        self.assertEqual(self.response.status_code, 200)
    def test_homepage_template(self):
        self.assertTemplateUsed(self.response, "blogpost/index.html")
    def test_homepage_contains_correct_html(self):
        self.assertContains(self.response, "Explore")
    def test_homepage_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, "Hi there! I should not be on the page.")
    # Create your tests here.
