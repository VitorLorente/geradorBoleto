import logging

from django.db import models
from django.utils.translation import gettext_lazy as _

from django_fsm import FSMField, transition
from postgres_copy import CopyManager

from . import utils
from .abstractionsChargeEmail import AbstractChargeGenerator, AbstractEmailSender, ModelABCMeta


logger = logging.getLogger(__name__)


class ChargesFile(models.Model):
    
    file = models.FileField(
        verbose_name=_("Arquivo CSV de boletos"),
        upload_to=utils.upload_to
    )
    uploadedAt = models.DateTimeField(
        verbose_name=_("Data e hora de upload do arquivo"),
        auto_now_add=True
    )


class ChargeState(models.TextChoices):
    IMPORTED = "IMPORTED", _("Imported")
    CHECKS_PASSED = "CHECKS_PASSED", _("Checks passed")
    CHECKS_UNPASSED = "CHECKS_UNPASSED", _("Checks unpassed")
    CHARGE_GENERATED = "CHARGE_GENERATED", _("Charge generated")
    EMAIL_SENT = "EMAIL_SENT", _("E-mail sent")


class Charge(
    models.Model,
    AbstractChargeGenerator,
    AbstractEmailSender,
    metaclass=ModelABCMeta
):
    
    source_file = models.ForeignKey(
        ChargesFile,
        verbose_name=_("Arquivo de origem do boleto"),
        on_delete=models.CASCADE
    )

    debtId = models.UUIDField(
        verbose_name=_("Id da cobrança recebido no arquivo"),
        max_length=38,
        primary_key=True,
        unique=True,
        null=False,
        blank=False,
        editable=False
    )
    name = models.CharField(
        verbose_name=_("Nome do sacado"),
        max_length=40,
        null=False,
        blank=False
    )
    governmentId = models.CharField(
        verbose_name=_("Número do boleto"),
        max_length=48,
        null=False,
        blank=False
    )
    email = models.EmailField(
        verbose_name=_("E-mail do sacado"),
        max_length=50,
        null=False,
        blank=False
    )
    debtAmount = models.DecimalField(
        verbose_name=_("Valor da cobrança"),
        max_digits=10,
        decimal_places=2,
        null=False,
        blank=False
    )
    debtDueDate = models.DateField(
        verbose_name=_("Data de vencimento da cobrança"),
        null=False,
        blank=False
    )

    stage = FSMField(
        default=ChargeState.IMPORTED,
        choices=ChargeState,
    )

    objects = CopyManager()


    @transition(
        field=stage, source=str(ChargeState.IMPORTED), target=str(ChargeState.CHECKS_PASSED)
    )
    def check_consistency_pass(self):
        """
        Nesta função podemos reforçar algumas verificações de consistência antes de realmente
        gerar os boletos. A lista de checks depende de requisitos detalhados de negócio. Abaixo,
        apenas um exemplo básico.
        """
        decimal_check = utils.validate_decimal(self.debtAmount)
        try:
            assert decimal_check
            return True
        except AssertionError:
            return False

    @transition(
        field=stage, source=str(ChargeState.CHECKS_PASSED), target=str(ChargeState.CHECKS_UNPASSED)
    )
    def check_consistency_unpass(self):
        pass

    @transition(
        field=stage, source=str(ChargeState.CHECKS_PASSED), target=str(ChargeState.CHARGE_GENERATED)
    )
    def generates_charge(self):
        doc_charge_number = "{}{}-{}".format(
            self.governmentId,
            self.debtDueDate.strftime("%Y%m%d"),
            str(self.debtAmount).replace(".", "")
        )

        GeneratedChargeDoc.objects.create(
            docChargeNumber=doc_charge_number,
            charge=self
        )

    @transition(
        field=stage, source=str(ChargeState.CHARGE_GENERATED), target=str(ChargeState.EMAIL_SENT)
    )
    def send_email(self):
        recipient = "\n\nPara:{}".format(self.email)
        subject = "\nAssunto: Boleto com vencimento em {}".format(
            self.debtDueDate.strftime("%d/%m/%Y")
        )
        message = "\nOlá, {}.\nSei que a vida não está fácil, então toma mais um boleto:\n{}\n\n".format(
            self.name,
            self.charge_doc.docChargeNumber
        )
        full_email = "{}{}{}".format(recipient, subject, message)
        logger.info(full_email)


class GeneratedChargeDoc(models.Model):

    docChargeNumber = models.CharField(
        verbose_name=_("Número do boleto gerado"),
        max_length=20
    )
    createdAt = models.DateTimeField(
        verbose_name=_("Data e hora de geração do arquivo"),
        auto_now_add=True
    )
    charge = models.OneToOneField(
        Charge,
        on_delete=models.CASCADE,
        related_name="charge_doc"
    )