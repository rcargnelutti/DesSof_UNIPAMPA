from django.forms import ModelForm

from condominio.models import Condominio, Unidade

class CondominioForm(ModelForm):
    class Meta:
        model = Condominio
        fields = ['nome', 'documento', 'cep', 'endereco', 'numero', 'bairro', 'cidade', 'estado', 'pais', 
                  'area_comum', 'area_privativa', 'area_total', 'dia_vencimento_boleto']


class UnidadeForm(ModelForm):
    class Meta:
        model = Unidade
        fields = ('nome',)