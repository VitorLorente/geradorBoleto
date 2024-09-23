from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from core.models import ChargesFile

class UploadCSVViewTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_get_request(self):
        response = self.client.get('/upload-csv/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"message": "Envie um arquivo CSV usando POST"})

    def test_post_request_with_valid_csv(self):
        with open('test.csv', 'w') as f:
            f.write("col1,col2\nvalue1,value2")

        with open('test.csv', 'rb') as file:
            response = self.client.post('/upload-csv/', {'file': file}, format='multipart')

        # Verifica se a resposta tem status 202
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

        charge_file = ChargesFile.objects.last()  # Obtém o arquivo mais recente salvo

        # Verifica se o nome do arquivo contém 'test.csv'
        self.assertIn('test', charge_file.file.name)

    def test_post_request_with_invalid_file(self):
        with open('test.txt', 'w') as f:
            f.write("invalid content")

        with open('test.txt', 'rb') as file:
            response = self.client.post('/upload-csv/', {'file': file})

        # Verifica se a resposta tem status 400 ou 404
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
