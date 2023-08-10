from django.test import TestCase
from django.contrib.auth import get_user_model

# Create your tests here.

class CustomUserTests(TestCase):
    '''
    Test to create users
    '''
    def test_create_user(self):
        User = get_user_model()
        User = User.objects.create(username="kendrick",email="kendricklamar@gmail.com", password="kendrick@343!")
        
        #assertions
        self.assertEqual(User.username,"kendrick")
        self.assertEqual(User.email,"kendricklamar@gmail.com")
        self.assertTrue(User.is_active)
        self.assertFalse(User.is_staff)
        self.assertFalse(User.is_superuser)
        
    def test_create_superuser(self):
        '''Test to create a superuser'''
        User = get_user_model()
        User = User.objects.create_superuser(username="j.cole", email="coleworld@gmail.com", password="jcole@334")
        
        #assertions
        self.assertEqual(User.username,"j.cole")
        self.assertEqual(User.email, "coleworld@gmail.com")
        self.assertTrue(User.is_active)
        self.assertTrue(User.is_staff)
        self.assertTrue(User.is_superuser)