from datetime import datetime
from decimal import Decimal

from django.test import TestCase
from django_fsm import TransitionNotAllowed
from core.models import Charge, ChargeState, GeneratedChargeDoc, ChargesFile
from unittest.mock import patch

class ChargeModelTestCase(TestCase):
    
    def setUp(self):
        self.charges_file = ChargesFile.objects.create(file='test.csv')
        self.charge = Charge.objects.create(
            source_file=self.charges_file,
            debtId='ea23f2ca-663a-4266-a742-9da4c9f4fcb3',
            name='Joana Darc',
            governmentId='1234',
            email='joanadarc@idademedia.com',
            debtAmount=Decimal("100.50"),
            debtDueDate=datetime.strptime('2024-12-31', '%Y-%m-%d'),
            stage=str(ChargeState.IMPORTED)  # Status inicial
        )

    @patch('core.utils.validate_decimal')
    def test_check_consistency_pass_success(self, mock_validate_decimal):
        mock_validate_decimal.return_value = True

        result = self.charge.check_consistency_pass()

        self.assertTrue(result)
        self.assertEqual(self.charge.stage, ChargeState.CHECKS_PASSED)

    @patch('core.utils.validate_decimal')
    def test_check_consistency_pass_failure(self, mock_validate_decimal):
        mock_validate_decimal.return_value = False

        result = self.charge.check_consistency_pass()
        if not result:
            self.charge.check_consistency_unpass()

        self.assertFalse(result)
        self.assertEqual(self.charge.stage, ChargeState.CHECKS_UNPASSED)

    def test_check_consistency_unpass(self):
        self.charge.stage = ChargeState.CHECKS_PASSED
        self.charge.save()

        self.charge.check_consistency_unpass()

        self.assertEqual(self.charge.stage, ChargeState.CHECKS_UNPASSED)

    def test_generates_charge_success(self):
        self.charge.stage = ChargeState.CHECKS_PASSED
        self.charge.save()

        self.charge.generates_charge()

        self.assertEqual(self.charge.stage, ChargeState.CHARGE_GENERATED)

        charge_doc = GeneratedChargeDoc.objects.get(charge=self.charge)
        expected_doc_number = "123420241231-10050"
        self.assertEqual(charge_doc.docChargeNumber, expected_doc_number)

    def test_generates_charge_fails_if_not_checks_passed(self):
        with self.assertRaises(TransitionNotAllowed):
            self.charge.generates_charge()