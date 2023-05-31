from django.forms import ModelForm
from condominio.models import Condominio, Unidade, Pessoa, PessoaUnidade, Conta, Despesa, Fatura  # noqa
from django import forms


class CondominioForm(ModelForm):
    class Meta:
        model = Condominio
        fields = ['nome', 'documento', 'cep', 'endereco', 'numero', 'bairro', 'cidade', 'estado', 'pais',  # noqa
                  'area_comum', 'area_privativa', 'area_total', 'dia_vencimento_boleto', 'multa', 'juro']  # noqa


class UnidadeForm(ModelForm):  # SEM CBV MÁSCARA E DEMAIS ATTRS FUNCIONA
    class Meta:
        model = Unidade
        fields = ('nome', 'fracao',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nome'].widget.attrs.update({'class': 'form-control', 'placeholder': ''})  # noqa
        self.fields['fracao'].widget.attrs.update({'class': 'form-control mask-fracao', 'placeholder': '_.________', 'style': 'width: 150px'})  # noqa


class PessoaForm(ModelForm):  # COM CBV MÁSCARA NÃO FUNCIONA
    class Meta:
        model = Pessoa
        fields = ('nome', 'documento', 'status',)


class PessoaUnidadeForm(ModelForm):
    class Meta:
        model = PessoaUnidade
        fields = ('pessoa', 'vinculo', 'data_inicio', 'data_fim',)  # noqa


class ContaForm(ModelForm):
    class Meta:
        model = Conta
        fields = ('descricao', 'status',)


class DespesaForm(ModelForm):
    valor = forms.DecimalField(max_digits=8, decimal_places=2, localize=True)

    def __init__(self, *args, **kwargs):
        condominio_id = kwargs.pop('condominio_id')
        super(DespesaForm, self).__init__(*args, **kwargs)
        self.fields['conta'].queryset = Conta.objects.filter(condominio_id=condominio_id).order_by('descricao')  # noqa

    class Meta:
        model = Despesa
        fields = ('conta', 'rateio', 'valor', 'data', 'identificacao',)  # noqa


class FaturaForm(forms.Form):
    data_inicio = forms.DateField()
    data_fim = forms.DateField()
    data_vencimento = forms.DateField()


class FaturaPagarForm(forms.Form):
    data_pagamento = forms.DateField()
    valor_multa = forms.DecimalField(max_digits=8, decimal_places=2, localize=True)  # noqa
    valor_juro = forms.DecimalField(max_digits=8, decimal_places=2, localize=True)  # noqa
    valor_pago = forms.DecimalField(max_digits=8, decimal_places=2, localize=True)  # noqa

    class Meta:
        model = Fatura
        fields = ('status', 'data_pagamento', 'valor_multa', 'valor_juro', 'valor_pago', 'dias_atraso_pagamento')  # noqa


class RelatorioForm(forms.Form):
    data_inicio = forms.DateField()
    data_fim = forms.DateField()
