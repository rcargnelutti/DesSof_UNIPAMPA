from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView  # noqa
from condominio.models import Condominio, Unidade, Pessoa, PessoaUnidade, Conta, Despesa  # noqa
from condominio.forms import UnidadeForm, PessoaUnidadeForm, ContaForm, DespesaForm  # noqa
from decimal import Decimal

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


# Fatura

def fatura_list(request, condominio_id):
    condominio = Condominio.objects.get(id=condominio_id)  # noqa
    return render(request, 'condominio/fatura_list.html', {'condominio': condominio})  # noqa


def fatura_create(request, condominio_id):
    ctx = {}
    # data_inicio = '2023-05-01'
    # data_fim = '2023-05-31'
    data_inicio = request.POST.get('data_inicio')
    data_fim = request.POST.get('data_fim')
    data_vencimento = request.POST.get('data_vencimento')
    if data_inicio and data_fim:
        condominio = Condominio.objects.get(id=condominio_id)  # noqa
        unidade = Unidade.objects.filter(condominio_id=condominio_id)  # noqa
        despesa = Despesa.objects.filter(condominio_id=condominio_id, data__range=(data_inicio, data_fim))  # noqa
        despesa.qtd = despesa.count()
        unidade.qtd = unidade.count()
        rateios = []
        val = [None,None,None,None,None]
        for u in unidade:
            total = 0
            pessoa_unidade = PessoaUnidade.objects.get(unidade_id=u.id)  # noqa
            pessoa = pessoa_unidade.pessoa
            # testar se tem proprietário e locatário
            print(u.nome, pessoa_unidade.pessoa, pessoa_unidade.vinculo)
            val[0] = u
            val[1] = pessoa_unidade
            for d in despesa:
                if d.rateio == 'Fração':
                    print(d.conta, " - ", ((d.valor) *
                          Decimal(u.fracao)).quantize(Decimal("0.00")))
                    valor = ((d.valor) * Decimal(u.fracao)
                             ).quantize(Decimal("0.00"))
                    total = total + valor
                if d.rateio == 'Unidade':
                    print(d.conta, " - ", d.valor / unidade.qtd)
                    valor = (d.valor / unidade.qtd)
                    total = total + valor
            print(total)
            val[2] = total
            val[3] = "05/2023"
            val[4] = data_vencimento
            rateios.append(val)
        print("Tipo da lista: ", type(rateios))
        ctx = {
            'condominio': condominio,
            'unidade': unidade,
            'despesa': despesa,
            'rateios': rateios,
        }

    if request.method == "GET":
        form = DespesaForm(initial={})
        return render(request, 'condominio/fatura_form.html', {'ctx': ctx, 'form': form})  # noqa
    else:
        form = DespesaForm(request.POST)
        if not form.is_valid():
            return render(request, 'condominio/fatura_form.html', {'ctx': ctx, 'form': form})  # noqa
        # despesa = form.save(commit=False)
        # despesa.condominio = condominio
        # despesa.save()
        return redirect(f'/condominios/fatura_list/{condominio_id}/')  # noqa


# Fatura Protótipo

def fatura_list2(request):
    return render(request, 'condominio/fatura_list2.html')  # noqa


def fatura_create2(request):
    return render(request, 'condominio/fatura_form2.html')  # noqa
