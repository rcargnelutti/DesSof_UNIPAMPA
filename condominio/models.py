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
    multa = models.DecimalField('multa (%):', max_digits=10, decimal_places=0)  # noqa
    juro = models.DecimalField('juro ao mês (%):', max_digits=10, decimal_places=0)  # noqa
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
        ATIVA = 'Ativa', 'Ativa'
        INATIVA = 'Inativa', 'Inativa'
    nome = models.CharField(max_length=200)
    documento = models.CharField('CPF', max_length=20)
    status = models.CharField(choices=Status.choices, default=Status.ATIVA, max_length=10)  # noqa
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome


class Morador(models.TextChoices):
    PROPRIETARIO = 'Proprietário', 'Proprietário'
    LOCATARIO = 'Locatário', 'Locatário'


class PessoaUnidade(models.Model):
    pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE, related_name="moradores")  # noqa
    unidade = models.ForeignKey(Unidade, on_delete=models.PROTECT, related_name="moradores")  # noqa
    vinculo = models.CharField(choices=Morador.choices, max_length=15)  # noqa
    data_inicio = models.DateField('data de início', null=True)
    data_fim = models.DateField('data de fim', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.pessoa} - {self.unidade}"


class Conta(models.Model):
    class Status(models.TextChoices):
        ATIVA = 'Ativa', 'Ativa'
        INATIVA = 'Inativa', 'Inativa'
    descricao = models.CharField(max_length=200)
    status = models.CharField(choices=Status.choices, default=Status.ATIVA, max_length=10)  # noqa
    condominio = models.ForeignKey(Condominio, on_delete=models.CASCADE, related_name='contas')  # noqa
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.descricao


class Despesa(models.Model):
    class Rateio(models.TextChoices):
        FRACAO = 'Fração', 'Fração'
        UNIDADE = 'Unidade', 'Unidade'
    condominio = models.ForeignKey(Condominio, on_delete=models.CASCADE, related_name='despesas')  # noqa
    conta = models.ForeignKey(Conta, on_delete=models.PROTECT, related_name="despesas")  # noqa
    rateio = models.CharField(choices=Rateio.choices, default=Rateio.FRACAO, max_length=10)  # noqa
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField(null=True)
    identificacao = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.conta


class StatusFatura(models.TextChoices):
    ABERTO = 'ABERTO'
    PAGO = 'PAGO'


class Fatura(models.Model):
    data_criacao = models.DateTimeField()
    data_inicio = models.DateField()
    data_fim = models.DateField()
    data_pagamento = models.DateField(blank=True, null=True)
    competencia_ano = models.IntegerField()
    competencia_mes = models.IntegerField()
    data_vencimento = models.DateField()
    unidade = models.ForeignKey(Unidade, related_name='faturas', on_delete=models.PROTECT)  # noqa
    proprietario = models.ForeignKey(Pessoa, related_name='faturas_proprietario', on_delete=models.PROTECT)  # noqa
    locatario = models.ForeignKey(Pessoa, null=True, blank=True, related_name='faturas_locatario', on_delete=models.PROTECT)  # noqa
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(choices=StatusFatura.choices, max_length=6)
    valor_multa = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # noqa
    valor_juro = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # noqa
    valor_pago = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # noqa
    dias_atraso_pagamento = models.IntegerField(blank=True, null=True)

    class Meta:
        unique_together = ['unidade', 'competencia_ano', 'competencia_mes']


class FaturaDespesa(models.Model):
    fatura = models.ForeignKey(Fatura, related_name='despesas', on_delete=models.CASCADE)  # noqa
    despesa = models.ForeignKey(Despesa, related_name='fatura_itens', on_delete=models.PROTECT)  # noqa
    valor = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ['fatura', 'despesa']


class Telefone(models.Model):
    pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE, related_name="contato_telefone")  # noqa
    descricao = models.CharField(max_length=200)
    numero = models.CharField('Número', max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.pessoa} - {self.descricao} - {self.numero}"


class Email(models.Model):
    pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE, related_name="contato_email")  # noqa
    descricao = models.CharField(max_length=200)
    endereco = models.CharField('E-mail', max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.pessoa} - {self.descricao} - {self.email}"
