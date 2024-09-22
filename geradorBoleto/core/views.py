from celery import chain
from celery.result import AsyncResult
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ChargesFile
from .serializers import CSVUploadSerializer
from . import tasks


class UploadCSVView(APIView):
    
    def get(self, request, *args, **kwargs):
        return Response(
            {"message": "Envie um arquivo CSV usando POST"},
            status=status.HTTP_200_OK
        )

    def post(self, request, *args, **kwargs):
        serializer = CSVUploadSerializer(data=request.data)

        if serializer.is_valid():
            file = serializer.validated_data['file']
            charge_file = ChargesFile.objects.create(
                file=file
            )

            chain(
                tasks.process_csv.s(
                    charge_file.file.path,
                    charge_file.pk
                ),
                tasks.performs_validation_checks.si(
                    charge_file.pk
                ),
                tasks.performs_charge_generation.si(
                    charge_file.pk
                ),
                tasks.performs_sending_emails.si(
                    charge_file.pk
                )
            ).apply_async()

            return Response(
                {
                    "file_name": charge_file.file.name,
                },
                status=status.HTTP_202_ACCEPTED
            )
        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
