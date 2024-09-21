import csv
from celery import shared_task
from django.db import transaction
from io import StringIO
from .models import Charge, ChargesFile

CHUNK_SIZE = 5000  # Defina o tamanho do chunk conforme necessário

@shared_task(bind=True)
def process_csv_task(self, csv_data, charge_file_pk):
    csv_file = StringIO(csv_data)
    reader = csv.DictReader(csv_file)
    charge_file = ChargesFile.objects.get(pk=charge_file_pk)
    rows_to_insert = []
    count = 0

    for row in reader:
        row['source_file'] = charge_file
        rows_to_insert.append(Charge(**row))
        count += 1
        
        if count % CHUNK_SIZE == 0:
            with transaction.atomic():
                Charge.objects.bulk_create(rows_to_insert)
            rows_to_insert = []
            print("\n\nsave\n\n")

    if rows_to_insert:
        with transaction.atomic():
            Charge.objects.bulk_create(rows_to_insert)
        print("ultimo save\n\n\n")
