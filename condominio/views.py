from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from condominio.models import Condominio, Unidade
from condominio.forms import UnidadeForm


# CONDOMÍNIO
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


def condominio_gestao(request, condominio_id):
    condominio = Condominio.objects.get(id=condominio_id)
    return render(request, 'condominio/condominio_gestao.html', {'object':condominio})


# UNIDADES


#def unidade_list(request, condominio_id):
def unidade_list(request):
    #condominio = Condominio.objects.get(id=condominio_id)
    data = {}
    data = request.GET.get('search')
    return render(request, 'condominio/unidade_list.html', data)
    #return render(request, 'condominio/unidade_list.html', data, {'object':condominio})


def unidade_create(request, condominio_id):
    condominio = Condominio.objects.get(id=condominio_id)

    if request.method == "GET":
        form = UnidadeForm(initial = {'condominio':condominio})
        return render(request, 'condominio/unidade_form.html', {'object':condominio, 'form': form})
    else:
        form = UnidadeForm(request.POST)
        if not form.is_valid():
            return render(request, 'condominio/unidade_form.html', {'object':condominio, 'form': form})
        unidade = form.save(commit=False)
        unidade.condominio = condominio
        unidade.save()
        return redirect(reverse('condominio:list'))