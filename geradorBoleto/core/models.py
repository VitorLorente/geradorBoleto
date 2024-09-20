from django.db import models


class ChargesFile(models.Model):
    
    file_name = models.CharField(
        verbose_name="Nome do arquivo",
        max_length=25
    )
    uploaded_at = models.DateTimeField(
        verbose_name="Data de upload do arquivo",
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
    # Este campo não está configurado como Primary Key pois não sei se este id é único mesmo
    # inclusive entre diferentes instituições de pagamentos. Portanto, preferi deixar explícito
    # que este id tem origem no arquivo recebido. O ID utilizado como identificador é o criado
    # automaticamente pelo Django

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
