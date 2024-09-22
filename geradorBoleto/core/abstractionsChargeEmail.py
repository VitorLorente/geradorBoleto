from abc import ABC, ABCMeta, abstractmethod

from django.db import models


class ModelABCMeta(ABCMeta, models.base.ModelBase):
    pass

class AbstractChargeGenerator(ABC):

    @abstractmethod
    def generates_charge(self):
        """
        Método que deverá ser implementada em Charge para geração boletos. No nosso caso,
        deverá apenas gerar um número qualquer, concatenando as infos da cobrança, como
        se estivesse gerando o número do boleto.
        """
        pass


class AbstractEmailSender(ABC):

    # @abstractmethod
    # def format_email(self):
    #     """
    #     Método responsável por colher as informações e formatar a string do e-mail.
    #     """
    #     pass

    @abstractmethod
    def send_email(self):
        """
        Método responsável por disparar o e-mail formatado. No nosso caso, apenas enviará
        um log com o texto do e-mail.
        """
        pass