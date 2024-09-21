from datetime import datetime

from django.db import models

from .utils import upload_to


class ChargesFile(models.Model):
    
    file = models.FileField(
        verbose_name="Arquivo CSV de boletos",
        upload_to=upload_to
    )
    uploadedAt = models.DateTimeField(
        verbose_name="Data e hora de upload do arquivo",
        auto_now_add=True
    )


class Charge(models.Model):
    
    source_file = models.ForeignKey(
        ChargesFile,
        verbose_name="Arquivo de origem do boleto",
        on_delete=models.CASCADE
    )

    debtId = models.CharField(
        verbose_name="Id da cobrança recebido no arquivo",
        max_length=38
    )

    name = models.CharField(
        verbose_name="Nome do sacado",
        max_length=40
    )
    governmentId = models.CharField(
        verbose_name="Número do boleto",
        max_length=48,
    )
    email = models.EmailField(
        verbose_name="E-mail do sacado",
        max_length=50
    )
    debtAmount = models.DecimalField(
        verbose_name="Valor da cobrança",
        max_digits=10,
        decimal_places=2
    )
    debtDueDate = models.DateField(
        verbose_name="Data de vencimento da cobrança"
    )
