# from django.core.files.base import ContentFile
# from django.test import TestCase
# from core.tasks import process_csv, performs_validation_checks, performs_charge_generation, performs_sending_emails
# from core.models import Charge, ChargesFile, ChargeState
# from unittest.mock import patch
# from io import StringIO
# import csv

# class CeleryTaskTestCase(TestCase):

#     def setUp(self):
#         csv_data = StringIO()
#         writer = csv.writer(csv_data)
#         writer.writerow(['name', 'governmentId', 'email', 'debtAmount', 'debtDueDate', 'debtId'])
#         writer.writerow(['Elijah Santos', '9558', 'janet95@example.com', '1000000', '2024-01-19', 'ea23f2ca-663a-4266-a742-9da4c9f4fcb3'])

#         # Salvar o CSV em um arquivo no formato que o Django espera
#         self.charge_file = ChargesFile.objects.create(file=ContentFile(csv_data.getvalue().encode('utf-8'), name='test.csv'))
        
#         # Criar uma instância de Charge
#         self.charge = Charge.objects.create(
#             source_file=self.charge_file,
#             stage=ChargeState.IMPORTED
#         )

#     @patch('core.tasks.open')
#     @patch('core.models.Charge.objects.from_csv')
#     def test_process_csv(self, mock_from_csv, mock_open):
#         # Mock de abrir o arquivo
#         header = "name,governmentId,email,debtAmount,debtDueDate,debtId\n"
#         line = "Elijah Santos,9558,janet95@example.com,1000000,2024-01-19,ea23f2ca-663a-4266-a742-9da4c9f4fcb3"
#         mock_open.return_value.__enter__.return_value = StringIO(
#            "{}{}".format(header, line)
#         )

#         # Executa a task
#         process_csv(file_path='test.csv', charge_file_pk=self.charge_file.pk)

#         # Verifica se o método from_csv foi chamado corretamente
#         mock_from_csv.assert_called_once()

#     def test_performs_validation_checks(self):
#         # Verifica que a task executa a validação corretamente
#         performs_validation_checks(self.charge_file.pk)

#         # Recarrega o objeto para verificar o estado
#         self.charge.refresh_from_db()

#         # Se a validação passou
#         self.assertEqual(self.charge.stage, ChargeState.CHECKS_PASSED)

#     def test_performs_charge_generation(self):
#         # Define o status como CHECKS_PASSED para permitir a transição
#         self.charge.stage = ChargeState.CHECKS_PASSED
#         self.charge.save()

#         # Executa a task
#         performs_charge_generation(self.charge_file.pk)

#         # Recarrega o objeto para verificar o estado
#         self.charge.refresh_from_db()
#         self.assertEqual(self.charge.stage, ChargeState.CHARGE_GENERATED)

#     def test_performs_sending_emails(self):
#         # Define o status como CHARGE_GENERATED para permitir a transição
#         self.charge.stage = ChargeState.CHARGE_GENERATED
#         self.charge.save()

#         # Executa a task
#         performs_sending_emails(self.charge_file.pk)

#         # Recarrega o objeto para verificar o estado
#         self.charge.refresh_from_db()
#         self.assertEqual(self.charge.stage, ChargeState.EMAIL_SENT)