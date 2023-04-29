from django.forms import ModelForm
from condominio.models import Condominio, Unidade, Pessoa, PessoaUnidade


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
        #data_inicio = forms.DateField(widget=forms.DateInput(format ='%d/%m/%Y'), input_formats=settings.DATE_INPUT_FORMATS) # noqa
        #data_fim = forms.DateField(widget=forms.DateInput(format ='%d/%m/%Y'), input_formats=settings.DATE_INPUT_FORMATS) # noqa

        widgets = {
            #'pessoa': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Pessoa', 'style': 'width: 250px'}), # noqa
            #'vinculo': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Vínculo', 'style': 'width: 250px'}), # noqa
            #'data_inicio': forms.TextInput (attrs={'class': 'form-control'}), # noqa
            #'data_fim': forms.TextInput(attrs={'class': 'form-control mask-date', 'placeholder': '__/__/____', 'style': 'width: 150px'}), # noqa
        }
