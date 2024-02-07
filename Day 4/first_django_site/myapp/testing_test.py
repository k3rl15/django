from django.test import TestCase, Client
from django.urls import reverse
from .models import Profile
import json


class ProfileAPITest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_create_profile(self):
        url = reverse('profiles')
        data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'mobile_number': '1234567890',
            'address': '123 Street'
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Profile.objects.filter(name='John Doe').exists())

    def test_get_profiles(self):
        Profile.objects.create(name='Test User', email='test@example.com')
        url = reverse('profiles')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), Profile.objects.count())

    def test_get_profile_detail(self):
        profile = Profile.objects.create(name='Test User', email='test@example.com')
        url = reverse('profile_detail', args=[profile.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], 'Test User')

    def test_update_profile(self):
        profile = Profile.objects.create(name='Test User', email='test@example.com')
        url = reverse('profile_detail', args=[profile.pk])
        data = {
            'name': 'Updated User',
            'email': 'updated@example.com'
        }
        response = self.client.put(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        updated_profile = Profile.objects.get(pk=profile.pk)
        self.assertEqual(updated_profile.name, 'Updated User')
        self.assertEqual(updated_profile.email, 'updated@example.com')

    def test_delete_profile(self):
        profile = Profile.objects.create(name='Test User', email='test@example.com')
        url = reverse('profile_detail', args=[profile.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Profile.objects.filter(pk=profile.pk).exists())
