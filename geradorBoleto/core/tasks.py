import csv

from celery import shared_task

from .models import Charge
from .utils import add_fk_column_generator, generate_csv_from_dict


@shared_task(bind=True)
def process_csv_task_copy(self, file_path, charge_file_pk):

    with open(file_path, mode='r') as csv_file:
        reader = csv.DictReader(csv_file)
        normalized_reader = [
            row for row in add_fk_column_generator(reader, charge_file_pk)
        ]

        output = generate_csv_from_dict(normalized_reader)

        Charge.objects.from_csv(
            output,
            dict(
                source_file="source_file",
                debtId="debtId",
                name="name",
                governmentId="governmentId",
                email="email",
                debtAmount="debtAmount",
                debtDueDate="debtDueDate"
            ),
            ignore_conflicts=True # Permite ignorar linhas com erro de unique constraint e salvar o restante
            drop_constraints=False # Permite ignorar constraints gerais
        )

