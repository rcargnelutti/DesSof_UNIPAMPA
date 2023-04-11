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
    area_comum = models.CharField('área comum', max_length=50, blank=True, null=True)
    area_privativa = models.CharField('área privativa', max_length=50, blank=True, null=True)
    area_total = models.CharField('área total', max_length=50, blank=True, null=True)
    
    dia_vencimento_boleto = models.CharField('Dia de vencimento da fatura', max_length=2)
    
    status = models.BooleanField(default=True, blank=True, null=True)
    data_inicio_contrato = models.DateTimeField(blank=True, null=True)
    data_fim_contrato = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome