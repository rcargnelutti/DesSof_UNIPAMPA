from django.forms import ModelForm
from condominio.models import Condominio, Unidade, Pessoa, PessoaUnidade, Conta


class CondominioForm(ModelForm):
    class Meta:
        model = Condominio
        fields = ['nome', 'documento', 'cep', 'endereco', 'numero', 'bairro', 'cidade', 'estado', 'pais',  # noqa
                  'area_comum', 'area_privativa', 'area_total', 'dia_vencimento_boleto']  # noqa


class UnidadeForm(ModelForm):  # SEM CBV MÁSCARA E DEMAIS ATTRS FUNCIONA
    class Meta:
        model = Unidade
        fields = ('nome', 'fracao',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nome'].widget.attrs.update({'class': 'form-control', 'placeholder': ''}) # noqa
        self.fields['fracao'].widget.attrs.update({'class': 'form-control mask-fracao', 'placeholder': '_.________', 'style': 'width: 150px'}) # noqa


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
