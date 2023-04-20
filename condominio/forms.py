from django.forms import ModelForm

from condominio.models import Condominio, Unidade, Pessoa


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
