import os
from datetime import datetime

def upload_to(instance, filename):
    filename_splitted = filename.split(".")
    filename = filename_splitted[0]
    file_extension = filename_splitted[1]
    datetime_sufix = datetime.now().strftime("%Y%m%d%H%M%S")

    filename = f"{filename}_{datetime_sufix}.{file_extension}"

    return filename
