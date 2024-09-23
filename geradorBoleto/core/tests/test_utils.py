from django.test import TestCase

from django.test import TestCase
from core.utils import upload_to, normalize_columns_generator, generate_csv_from_dict, validate_decimal
from datetime import datetime
from decimal import Decimal


class UtilsTestCase(TestCase):

    def test_upload_to(self):
        # Testa se o nome do arquivo foi renomeado corretamente
        instance = None
        filename = "example.csv"
        result = upload_to(instance, filename)
        datetime_suffix = datetime.now().strftime("%Y%m%d%H%M")
        
        # Verifica se o arquivo foi renomeado corretamente
        self.assertTrue(result.startswith("example_"))
        self.assertTrue(result.endswith(".csv"))
        self.assertIn(datetime_suffix, result)

    def test_normalize_columns_generator(self):
        # Mock de um CSV Reader
        dict_reader = [
            {"col1": "value1", "col2": "value2"},
            {"col1": "value3", "col2": "value4"}
        ]
        pk = 1

        # Gera o resultado da função
        result = list(normalize_columns_generator(dict_reader, pk))

        # Verifica se as colunas foram normalizadas corretamente
        expected_result = [
            {"col1": "value1", "col2": "value2", "source_file": 1, "stage": "IMPORTED"},
            {"col1": "value3", "col2": "value4", "source_file": 1, "stage": "IMPORTED"}
        ]
        self.assertEqual(result, expected_result)

    def test_generate_csv_from_dict(self):
        data = [
            {"col1": "value1", "col2": "value2"},
            {"col1": "value3", "col2": "value4"}
        ]

        # Gera o CSV
        output = generate_csv_from_dict(data)

        # Esperado como resultado
        expected_output = "col1,col2\r\nvalue1,value2\r\nvalue3,value4\r\n"
        self.assertEqual(output.getvalue(), expected_output)

    def test_validate_decimal(self):
        # Teste para valores válidos
        self.assertTrue(validate_decimal(Decimal("123.45")))
        self.assertTrue(validate_decimal(Decimal("99999.99")))

        # Teste para valores inválidos
        self.assertFalse(validate_decimal("invalid"))
        self.assertFalse(validate_decimal(Decimal("100000.00")))