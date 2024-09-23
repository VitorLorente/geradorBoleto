from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from core.serializers import CSVUploadSerializer

class CSVUploadSerializerTestCase(TestCase):

    def test_valid_csv_file(self):
        file = SimpleUploadedFile("test.csv", b"col1,col2\nvalue1,value2", content_type="text/plain")
        serializer = CSVUploadSerializer(data={'file': file})

        self.assertTrue(serializer.is_valid())

    def test_invalid_file_type(self):
        file = SimpleUploadedFile("test.txt", b"invalid content", content_type="text/plain")
        serializer = CSVUploadSerializer(data={'file': file})

        self.assertFalse(serializer.is_valid())
        self.assertIn('Este arquivo não é um CSV.', serializer.errors['file'])