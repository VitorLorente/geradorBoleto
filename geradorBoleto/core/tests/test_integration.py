from decimal import Decimal
from datetime import datetime
from tempfile import NamedTemporaryFile

from django.test import TestCase
from core.models import Charge, ChargesFile, ChargeState
from core.tasks import (
    process_csv, performs_validation_checks, performs_charge_generation,
    performs_sending_emails
)

class CeleryIntegrationTestCase(TestCase):

    def setUp(self):
        header = "name,governmentId,email,debtAmount,debtDueDate,debtId\n"
        line = "Elijah Santos,9558,janet95@example.com,1000000,2024-01-19,ea23f2ca-663a-4266-a742-9da4c9f4fcb3"
        file_content = f"{header}{line}"

        self.temp_file = NamedTemporaryFile(delete=True, suffix='.csv')
        self.temp_file.write(str.encode(file_content))
        self.temp_file.seek(0)
        
        self.charge_file = ChargesFile.objects.create(file=self.temp_file.name)
        self.charge = Charge.objects.create(
            source_file=self.charge_file,
            debtId='ea23f2ca-663a-4266-a742-9da4c9f4fcb3',
            name='Joana Darc',
            governmentId='1234',
            email='joanadarc@idademedia.com',
            debtAmount=Decimal("100.50"),
            debtDueDate=datetime.strptime('2024-12-31', '%Y-%m-%d'),
            stage=str(ChargeState.IMPORTED)  # Status inicial
        )

    def test_full_csv_processing(self):
        # Executa todas as tasks em sequência
        process_csv(file_path=self.temp_file.name, charge_file_pk=self.charge_file.pk)
        performs_validation_checks(self.charge_file.pk)
        performs_charge_generation(self.charge_file.pk)
        performs_sending_emails(self.charge_file.pk)

        # Verifica se o Charge passou por todos os estágios corretamente
        self.charge.refresh_from_db()
        self.assertEqual(self.charge.stage, ChargeState.EMAIL_SENT)