from django.test import TestCase
from django.urls import reverse
from .models import Post, Category
from django.contrib.auth import get_user_model
from allauth.socialaccount.models import SocialApp
from dotenv import load_dotenv
import os
load_dotenv()
    # Create your tests here.
class BlogpostTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # user setup
        cls.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        
        # Create a SocialApp for your provider
        SocialApp.objects.create(
            provider='github',
            name='github',
            client_id=os.environ.get('SOCIAL_AUTH_GITHUB_KEY'),
            secret=os.environ.get('SOCIAL_AUTH_GITHUB_SECRET'),
        )
        # Category setup
        cls.category = Category.objects.create(name='front-end technology')
        
        cls.post = Post.objects.create(
        title="How to install and use django",
        author=cls.user,
        subtitle = 'Django the best backend framework',
    )
        cls.post.categories.set([cls.category])
    
    def test_blogpost_listing(self):
        self.assertEqual(f"{self.post.title}", "How to install and use django")
        self.assertEqual(f"{self.post.author}", "testuser")
        self.assertEqual(f"{self.post.subtitle}", "Django the best backend framework")
        self.assertEqual(self.post.categories.first().name, "front-end technology")
    def test_blogpost_list_view(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        print(response.content.decode()) 
        self.assertContains(response, "How to install and use django")
        self.assertTemplateUsed(response, "blogpost/index.html") 
        
    def test_blogpost_detail_view(self):
        response = self.client.get(self.post.get_absolute_url(), follow=True)
        no_response = self.client.get("/posts/12345/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "How to install and use django")
        self.assertTemplateUsed(response, "blogpost/blogpost_detail.html")   