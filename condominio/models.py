from django.db import models


class Condominio(models.Model):
    nome = models.CharField(max_length=200)
    documento = models.CharField('CNPJ', max_length=20)
    cep = models.CharField('CEP', max_length=10)
    endereco = models.CharField('Endereço', max_length=50)
    numero = models.CharField('Número', max_length=10)
    bairro = models.CharField(max_length=50)
    cidade = models.CharField(max_length=50)
    estado = models.CharField(max_length=50)
    pais = models.CharField('País', max_length=50)
    area_comum = models.CharField('área comum', max_length=50, blank=True, null=True)  # noqa
    area_privativa = models.CharField('área privativa', max_length=50, blank=True, null=True)  # noqa
    area_total = models.CharField('área total', max_length=50, blank=True, null=True)  # noqa

    dia_vencimento_boleto = models.CharField('Dia de vencimento da fatura', max_length=2)  # noqa

    status = models.BooleanField(default=True, blank=True, null=True)
    data_inicio_contrato = models.DateTimeField(blank=True, null=True)
    data_fim_contrato = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome


class Unidade(models.Model):
    nome = models.CharField(max_length=200)
    fracao = models.CharField('fração', max_length=20)
    condominio = models.ForeignKey(Condominio, on_delete=models.CASCADE, related_name='unidades')  # noqa


class Pessoa(models.Model):
    class Status(models.TextChoices):
        ATIVO = 'Ativo', 'Ativo'
        INATIVO = 'Inativo', 'Inativo'
    nome = models.CharField(max_length=200)
    documento = models.CharField('CPF', max_length=20)
    status = models.CharField(choices=Status.choices, default=Status.ATIVO, max_length=10)  # noqa
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome


class PessoaUnidade(models.Model):
    class Morador(models.TextChoices):
        PROPRIETARIO = 'Proprietário', 'Proprietário'
        LOCATARIO = 'Locatário', 'Locatário'
    pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE, related_name="moradores")  # noqa
    unidade = models.ForeignKey(Unidade, on_delete=models.PROTECT, related_name="moradores")  # noqa
    vinculo = models.CharField(choices=Morador.choices, max_length=15)  # noqa
    data_inicio = models.DateTimeField('data de início', null=True)
    data_fim = models.DateTimeField('data de fim', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.pessoa} - {self.unidade}"
