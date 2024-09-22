import csv
import re
from datetime import datetime
from decimal import Decimal, InvalidOperation
from io import StringIO


def upload_to(instance, filename):
    filename_splitted = filename.split(".")
    filename = filename_splitted[0]
    file_extension = filename_splitted[1]
    datetime_sufix = datetime.now().strftime("%Y%m%d%H%M%S")

    filename = f"{filename}_{datetime_sufix}.{file_extension}"

    return filename


def normalize_columns_generator(dict_reader, pk):
    for row in dict_reader:
        yield dict(row, **{'source_file': pk, 'stage': "IMPORTED"})


def generate_csv_from_dict(data):
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)

    output.seek(0)

    return output


def validate_decimal(value):
    try:
        Decimal(value)
    except InvalidOperation:
        return False
    return value <= Decimal("99999.99") # valor máximo que cabe num boleto
    