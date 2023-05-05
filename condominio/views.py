from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView  # noqa
from condominio.models import Condominio, Unidade, Pessoa, PessoaUnidade, Conta, Despesa
from condominio.forms import UnidadeForm, PessoaUnidadeForm, ContaForm, DespesaForm
import locale

# CONDOMÍNIO
class CondominioList(ListView):
    model = Condominio
    queryset = Condominio.objects.all()


class CondominioCreate(CreateView):
    model = Condominio
    fields = ['nome', 'documento', 'cep', 'endereco', 'numero', 'bairro', 'cidade', 'estado', 'pais',  # noqa
              'area_comum', 'area_privativa', 'area_total', 'dia_vencimento_boleto']  # noqa
    success_url = reverse_lazy('condominio:list')


class CondominioUpdate(UpdateView):
    model = Condominio
    fields = fields = ['nome', 'documento', 'cep', 'endereco', 'numero', 'bairro', 'cidade', 'estado', 'pais',  # noqa
                       'area_comum', 'area_privativa', 'area_total', 'dia_vencimento_boleto']  # noqa
    success_url = reverse_lazy('condominio:list')


class CondominioDetail(DetailView):
    queryset = Condominio.objects.all()


class CondominioDelete(DeleteView):
    queryset = Condominio.objects.all()
    success_url = reverse_lazy('condominio:list')


def condominio_gestao(request, condominio_id):
    condominio = Condominio.objects.get(id=condominio_id)
    return render(request, 'condominio/condominio_gestao.html', {'condominio': condominio})  # noqa


# UNIDADES


def unidade_list(request, condominio_id):
    condominio = Condominio.objects.get(id=condominio_id)
    unidade = Unidade.objects.order_by("nome").filter(condominio_id=condominio_id)  # noqa
    return render(request, 'condominio/unidade_list.html', {'unidade': unidade, 'condominio': condominio})  # noqa


def unidade_create(request, condominio_id):
    condominio = Condominio.objects.get(id=condominio_id)

    if request.method == "GET":
        form = UnidadeForm(initial={'condominio': condominio})
        return render(request, 'condominio/unidade_form.html', {'condominio': condominio, 'form': form})  # noqa
    else:
        form = UnidadeForm(request.POST)
        if not form.is_valid():
            return render(request, 'condominio/unidade_form.html', {'condominio': condominio, 'form': form})  # noqa
        unidade = form.save(commit=False)
        unidade.condominio = condominio
        unidade.save()
        return redirect(f'/condominios/unidade_list/{condominio_id}/')  # noqa


def unidade_update(request, unidade_id):
    unidade = Unidade.objects.get(id=unidade_id)
    condominio = unidade.condominio

    if request.method == "GET":
        form = UnidadeForm(instance=unidade)
        return render(request, 'condominio/unidade_form.html', {'condominio': condominio, 'form': form})  # noqa
    else:
        form = UnidadeForm(request.POST, instance=unidade)
        if not form.is_valid():
            return render(request, 'condominio/unidade_form.html', {'condominio': condominio, 'form': form})  # noqa
        form.save()
        return redirect(f'/condominios/unidade_list/{unidade.condominio_id}/')  # noqa


def unidade_confirm_delete(request, unidade_id):
    unidade = Unidade.objects.get(pk=unidade_id)
    return render(request, 'condominio/unidade_confirm_delete.html', {'unidade': unidade})  # noqa


def unidade_delete(request, unidade_id):
    unidade = Unidade.objects.get(pk=unidade_id)
    unidade.delete()
    return redirect(f'/condominios/unidade_list/{unidade.condominio_id}/')  # noqa


# PESSOAS

class PessoaList(ListView):
    model = Pessoa
    queryset = Pessoa.objects.all()


class PessoaCreate(CreateView):
    model = Pessoa
    fields = ['nome', 'documento', 'status']  # noqa
    success_url = reverse_lazy('condominio:pessoa_list')


class PessoaUpdate(UpdateView):
    model = Pessoa
    fields = fields = ['nome', 'documento', 'status']  # noqa
    success_url = reverse_lazy('condominio:pessoa_list')


class PessoaDetail(DetailView):
    queryset = Pessoa.objects.all()


# PESSOAUNIDADE - VINCULO / MORADOR

def pessoa_unidade_list(request, unidade_id):
    unidade = Unidade.objects.get(id=unidade_id)  # noqa
    pessoa_unidade = PessoaUnidade.objects.order_by("data_fim").filter(unidade_id=unidade_id)  # noqa
    return render(request, 'condominio/pessoa_unidade_list.html', {'unidade': unidade, 'pessoa_unidade': pessoa_unidade})  # noqa


def pessoa_unidade_create(request, unidade_id):
    unidade = Unidade.objects.get(id=unidade_id)

    if request.method == "GET":
        form = PessoaUnidadeForm(initial={'unidade': unidade})
        return render(request, 'condominio/pessoa_unidade_form.html', {'unidade': unidade, 'form': form})  # noqa
    else:
        form = PessoaUnidadeForm(request.POST)
        if not form.is_valid():
            return render(request, 'condominio/pessoa_unidade_form.html', {'unidade': unidade, 'form': form})  # noqa
        pessoa_unidade = form.save(commit=False)
        pessoa_unidade.unidade = unidade
        pessoa_unidade.save()
        return redirect(f'/condominios/pessoa_unidade_list/{unidade_id}/')  # noqa


def pessoa_unidade_update(request, pessoa_unidade_id):
    pessoa_unidade = PessoaUnidade.objects.get(id=pessoa_unidade_id)
    unidade = pessoa_unidade.unidade

    if request.method == "GET":
        form = PessoaUnidadeForm(instance=pessoa_unidade)
        return render(request, 'condominio/pessoa_unidade_form.html', {'unidade': unidade, 'form': form})  # noqa
    else:
        form = PessoaUnidadeForm(request.POST, instance=pessoa_unidade)
        if not form.is_valid():
            return render(request, 'condominio/pessoa_unidade_form.html', {'unidade': unidade, 'form': form})  # noqa
        form.save()
        return redirect(f'/condominios/pessoa_unidade_list/{pessoa_unidade.unidade_id}/')  # noqa


# CONTA

def conta_list(request, condominio_id):
    condominio = Condominio.objects.get(id=condominio_id)
    conta = Conta.objects.order_by("descricao").filter(condominio_id=condominio_id)  # noqa
    return render(request, 'condominio/conta_list.html', {'condominio': condominio, 'conta': conta})  # noqa


def conta_create(request, condominio_id):
    condominio = Condominio.objects.get(id=condominio_id)

    if request.method == "GET":
        form = ContaForm(initial={'condominio': condominio})
        return render(request, 'condominio/conta_form.html', {'condominio': condominio, 'form': form})  # noqa
    else:
        form = ContaForm(request.POST)
        if not form.is_valid():
            return render(request, 'condominio/conta_form.html', {'condominio': condominio, 'form': form})  # noqa
        conta = form.save(commit=False)
        conta.condominio = condominio
        conta.save()
        return redirect(f'/condominios/despesa_create/{condominio_id}/')


def conta_update(request, conta_id):
    conta = Conta.objects.get(id=conta_id)
    condominio = conta.condominio

    if request.method == "GET":
        form = ContaForm(instance=conta)
        return render(request, 'condominio/conta_form.html', {'condominio': condominio, 'form': form})  # noqa
    else:
        form = ContaForm(request.POST, instance=conta)
        if not form.is_valid():
            return render(request, 'condominio/conta_form.html', {'condominio': condominio, 'form': form})  # noqa
        form.save()
        return redirect(f'/condominios/despesa_create/{conta.condominio_id}/')  # noqa


# DESPESA

def despesa_list(request, condominio_id):
    condominio = Condominio.objects.get(id=condominio_id)  # noqa
    despesa = Despesa.objects.order_by("data").filter(condominio_id=condominio_id)  # noqa
    return render(request, 'condominio/despesa_list.html', {'condominio': condominio, 'despesa': despesa})  # noqa


def despesa_create(request, condominio_id):
    condominio = Condominio.objects.get(id=condominio_id)
    
    if request.method == "GET":
        form = DespesaForm(initial={'condominio': condominio})
        return render(request, 'condominio/despesa_form.html', {'condominio': condominio, 'form': form})  # noqa
    else:
        form = DespesaForm(request.POST)
        if not form.is_valid():
            return render(request, 'condominio/despesa_form.html', {'condominio': condominio, 'form': form})  # noqa
        despesa = form.save(commit=False)
        despesa.condominio = condominio
        despesa.save()
        return redirect(f'/condominios/despesa_list/{condominio_id}/')  # noqa


def despesa_update(request, despesa_id):
    despesa = Despesa.objects.get(id=despesa_id)
    condominio = despesa.condominio

    if request.method == "GET":
        form = DespesaForm(instance=despesa)
        return render(request, 'condominio/despesa_form.html', {'condominio': condominio, 'form': form})  # noqa
    else:
        form = DespesaForm(request.POST, instance=despesa)
        if not form.is_valid():
            return render(request, 'condominio/despesa_form.html', {'condominio': condominio, 'form': form})  # noqa
        form.save()
        return redirect(f'/condominios/despesa_list/{despesa.condominio_id}/')  # noqa


def despesa_confirm_delete(request, despesa_id):
    despesa = Despesa.objects.get(pk=despesa_id)
    return render(request, 'condominio/despesa_confirm_delete.html', {'despesa': despesa})  # noqa


def despesa_delete(request, despesa_id):
    despesa = Despesa.objects.get(pk=despesa_id)
    despesa.delete()
    return redirect(f'/condominios/despesa_list/{despesa.condominio_id}/')  # noqa

# Despesa

def receita_despesa_list(request):
    return render(request, 'condominio/receita_despesa_list.html')  # noqa


def receita_despesa_create(request):
    return render(request, 'condominio/receita_despesa_form.html')  # noqa


# Fatura

def fatura_list(request):
    return render(request, 'condominio/fatura_list.html')  # noqa


def fatura_create(request):
    return render(request, 'condominio/fatura_form.html')  # noqa
