from django.forms import ModelForm
from django import forms
import datetime
from django.conf import settings

from condominio.models import Condominio, Unidade, Pessoa, PessoaUnidade


class CondominioForm(ModelForm):
    class Meta:
        model = Condominio
        fields = ['nome', 'documento', 'cep', 'endereco', 'numero', 'bairro', 'cidade', 'estado', 'pais',  # noqa
                  'area_comum', 'area_privativa', 'area_total', 'dia_vencimento_boleto']  # noqa


class UnidadeForm(ModelForm):
    class Meta:
        model = Unidade
        fields = ('nome', 'fracao',)


class PessoaForm(ModelForm):
    class Meta:
        model = Pessoa
        fields = ('nome', 'documento', 'status',)


class PessoaUnidadeForm(ModelForm):
    class Meta:
        model = PessoaUnidade
        fields = ('vinculo', 'data_inicio', 'data_fim',)  # noqa
        data_inicio = forms.DateField(widget=forms.DateInput(format = '%d/%m/%Y'), input_formats=settings.DATE_INPUT_FORMATS)
        data_fim = forms.DateField(widget=forms.DateInput(format = '%d/%m/%Y'), input_formats=settings.DATE_INPUT_FORMATS)

