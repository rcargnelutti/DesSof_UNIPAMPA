from django.forms import ModelForm

from condominio.models import Condominio

class CondominioForm(ModelForm):
    class Meta:
        model = Condominio
        fields = ['nome', 'documento', 'cep', 'endereco', 'numero', 'bairro', 'cidade', 'estado', 'pais', 
                  'area_comum', 'area_privativa', 'area_total', 'dia_vencimento_boleto']

