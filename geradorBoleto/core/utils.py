import csv
from datetime import datetime
from io import StringIO


def upload_to(instance, filename):
    filename_splitted = filename.split(".")
    filename = filename_splitted[0]
    file_extension = filename_splitted[1]
    datetime_sufix = datetime.now().strftime("%Y%m%d%H%M%S")

    filename = f"{filename}_{datetime_sufix}.{file_extension}"

    return filename


def add_fk_column_generator(dict_reader, pk):
    for row in dict_reader:
        yield dict(row, **{'source_file': pk})


def generate_csv_from_dict(data):
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)

    output.seek(0)

    return output