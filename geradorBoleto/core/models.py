from datetime import datetime

from django.db import models

from .utils import upload_to


class ChargesFile(models.Model):
    
    file = models.FileField(
        verbose_name="Arquivo CSV de boletos",
        upload_to=upload_to
    )
    uploaded_at = models.DateTimeField(
        verbose_name="Data e hora de upload do arquivo",
        auto_now_add=True
    )


class Charge(models.Model):
    
    source_file = models.ForeignKey(
        ChargesFile,
        verbose_name="Arquivo de origem do boleto",
        on_delete=models.CASCADE
    )

    debt_id_from_file = models.CharField(
        verbose_name="Id da cobrança recebido no arquivo",
        max_length=38
    )

    debtor_name = models.CharField(
        verbose_name="Nome do sacado",
        max_length=40
    )
    government_id = models.CharField(
        verbose_name="Número do boleto",
        max_length=48,
    )
    debtor_email = models.EmailField(
        verbose_name="E-mail do sacado",
        max_length=30
    )
    debt_amount = models.DecimalField(
        verbose_name="Valor da cobrança",
        max_digits=10,
        decimal_places=2
    )
    debt_due_date = models.DateField(
        verbose_name="Data de vencimento da cobrança"
    )
