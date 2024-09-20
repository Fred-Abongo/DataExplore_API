from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from .models import UploadedFile

class DataSummaryAPITestCase(APITestCase):
    def setUp(self):
        # Simulate uploading a file and saving its metadata
        self.uploaded_file = UploadedFile.objects.create(
            name='test.csv',
            size=1000,
            data_id='12345-uuid'
        )

    def test_summary_statistics(self):
        url = reverse('data-summary', args=['12345-uuid'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('mean', response.data)
        self.assertIn('median', response.data)
        self.assertIn('mode', response.data)

    def test_file_not_found(self):
        url = reverse('data-summary', args=['nonexistent-uuid'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
