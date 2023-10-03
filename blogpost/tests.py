from django.test import TestCase
from django.urls import reverse
from .models import Post
    # Create your tests here.
class BookTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.post = Post.objects.create(
        title="How to install and use django",
        author="Frank Alimimian",
        subtitle = ' Django the best backend framework',
        categories ='front-end technology'
    )
    
    def test_book_listing(self):
        self.assertEqual(f"{self.post.title}", "How to install and use django")
        self.assertEqual(f"{self.post.author}", "Frank Alimimian")
        self.assertEqual(f"{self.post.subtitle}", "Django the best backend framework")
        self.assertEqual(f"{self.post.categories}", "front-end technology")
        
    def test_book_list_view(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "How to install and use Django")
        self.assertTemplateUsed(response, "blogpost/index.html") 
        
    def test_book_detail_view(self):
        response = self.client.get(self.post.get_absolute_url())
        no_response = self.client.get("/posts/12345/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "How to install and use Django")
        self.assertTemplateUsed(response, "blogpost/blogpost_detail.html")   