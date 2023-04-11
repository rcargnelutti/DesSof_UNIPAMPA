from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from condominio.models import Condominio


class CondominioList(ListView):
    model = Condominio
    queryset = Condominio.objects.all()


class CondominioCreate(CreateView):
    model = Condominio
    fields = ['nome', 'documento', 'cep', 'endereco', 'numero', 'bairro', 'cidade', 'estado', 'pais', 
                  'area_comum', 'area_privativa', 'area_total', 'dia_vencimento_boleto']
    success_url = reverse_lazy('condominio:list')


class CondominioUpdate(UpdateView):
    model = Condominio
    fields = fields = ['nome', 'documento', 'cep', 'endereco', 'numero', 'bairro', 'cidade', 'estado', 'pais', 
                  'area_comum', 'area_privativa', 'area_total', 'dia_vencimento_boleto']
    success_url = reverse_lazy('condominio:list')


class CondominioDetail(DetailView):
    queryset = Condominio.objects.all()


class CondominioDelete(DeleteView):
    queryset = Condominio.objects.all()
    success_url = reverse_lazy('condominio:list')