from django.forms import ModelForm
from django import forms
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
        fields = ('pessoa', 'vinculo', 'data_inicio', 'data_fim',)  # noqa
        data_inicio = forms.DateField(widget=forms.DateInput(format ='%d/%m/%Y'), input_formats=settings.DATE_INPUT_FORMATS) # noqa
        data_fim = forms.DateField(widget=forms.DateInput(format ='%d/%m/%Y'), input_formats=settings.DATE_INPUT_FORMATS) # noqa

        widgets = {
            'pessoa': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Pessoa', 'style': 'width: 250px'}), # noqa
            'vinculo': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Vínculo', 'style': 'width: 250px'}), # noqa
            'data_inicio': forms.TextInput (attrs={'class': 'form-control', 'placeholder': '__/__/____', 'style': 'width: 150px'}), # noqa
            'data_fim': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '__/__/____', 'style': 'width: 150px'}), # noqa
        }
