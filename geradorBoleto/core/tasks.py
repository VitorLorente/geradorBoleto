import csv

from celery import shared_task
from django.db import transaction

from .models import Charge
from .utils import normalize_columns_generator, generate_csv_from_dict


@shared_task(bind=True)
def process_csv(self, file_path, charge_file_pk):

    with open(file_path, mode='r') as csv_file:
        reader = csv.DictReader(csv_file)
        normalized_reader = [
            row for row in normalize_columns_generator(reader, charge_file_pk)
        ]
        output = generate_csv_from_dict(normalized_reader)

        Charge.objects.from_csv(
            output,
            ignore_conflicts=True, # Permite ignorar linhas com erro de unique constraint e salvar o restante
            drop_constraints=True # Permite ignorar constraints gerais
        )


@shared_task(bind=True)
def execute_validation_checks(self, charge_file_pk):
    charges = Charge.objects.filter(source_file__pk=charge_file_pk)

    for charge in charges:
        check = charge.check_consistency_pass()
        if not check:
            charge.check_consistency_unpass()
        charge.save()