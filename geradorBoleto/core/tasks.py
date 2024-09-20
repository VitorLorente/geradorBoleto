import csv
from celery import shared_task
from django.db import transaction
from io import StringIO
# from .models import YourModel  # Substitua pelo seu modelo real

CHUNK_SIZE = 1000  # Defina o tamanho do chunk conforme necessário

@shared_task(bind=True)
def process_csv_task(self, csv_data):
   print(
      "\n\n\n\nOI!!!\n\n\n\n",
      csv_data
   )
   pass
    # csv_file = StringIO(csv_data)
    # reader = csv.DictReader(csv_file)

    # rows_to_insert = []
    # count = 0

    # for row in reader:
    #     # Construa a instância do modelo com base nos dados do CSV
    #     rows_to_insert.append(YourModel(**row))
    #     count += 1
        
    #     # Insere em chunks
    #     if count % CHUNK_SIZE == 0:
    #         with transaction.atomic():
    #             YourModel.objects.bulk_create(rows_to_insert)
    #         rows_to_insert = []

    # # Insere o último chunk
    # if rows_to_insert:
    #     with transaction.atomic():
    #         YourModel.objects.bulk_create(rows_to_insert)