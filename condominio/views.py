#from django.db.models import OuterRef, Subquery
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView  # noqa
from condominio.models import Condominio, Unidade, Pessoa, PessoaUnidade, Conta, Despesa, Fatura, Morador, FaturaDespesa, StatusFatura  # noqa
from condominio.forms import UnidadeForm, PessoaUnidadeForm, ContaForm, DespesaForm, FaturaForm, FaturaPagarForm  # noqa
from decimal import Decimal
from django.http import JsonResponse

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
    qtd_faturas_atraso = faturas_em_atraso(condominio_id)
    qtd_faturas_aberto = faturas_em_aberto(condominio_id)
    context = {
        'condominio': condominio, 
        'qtd_faturas_atraso': qtd_faturas_atraso,
        'qtd_faturas_aberto': qtd_faturas_aberto, 
    }
    return render(request, 'condominio/condominio_gestao.html', context)  # noqa


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
        form = DespesaForm(initial={'condominio': condominio}, condominio_id=condominio_id) # noqa
        return render(request, 'condominio/despesa_form.html', {'condominio': condominio, 'form': form})  # noqa
    else:
        form = DespesaForm(request.POST, condominio_id=condominio_id)
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
        form = DespesaForm(instance=despesa, condominio_id=condominio)
        return render(request, 'condominio/despesa_form.html', {'condominio': condominio, 'form': form})  # noqa
    else:
        form = DespesaForm(request.POST, instance=despesa, condominio_id=condominio) # noqa
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
    condominio = get_object_or_404(Condominio, pk=condominio_id)
    ids_unidades = condominio.unidades.all().values('pk')
    faturas = Fatura.objects\
        .select_related('unidade', 'proprietario', 'locatario')\
        .filter(unidade_id__in=ids_unidades)\
        .order_by('status', '-data_vencimento')
    for fatura in faturas:
        fatura.despesas_list = fatura.despesas.select_related('despesa__conta').all()
    total_faturas = len(faturas)
    context = {'condominio': condominio, 'faturas': faturas, 'total_faturas': total_faturas}
    return render(request, 'condominio/fatura_list.html', context)


def fatura_create(request, condominio_id):
    ctx = {}
    condominio = get_object_or_404(Condominio, pk=condominio_id)
    if request.method == 'POST':
        form = FaturaForm(request.POST)
        if not form.is_valid():
            ctx['erro_formulario'] = "Formulário inválido"
        else:
            data_criacao = timezone.now()
            data_inicio = form.cleaned_data['data_inicio']
            data_fim = form.cleaned_data['data_fim']
            data_vencimento = form.cleaned_data['data_vencimento']
            #pessoa_subquery = PessoaUnidade.objects.filter(unidade_id=OuterRef('pk'))
            # proprietario_subquery = pessoa_subquery.filter(vinculo=Morador.PROPRIETARIO.value)
            # locatario_subquery = pessoa_subquery.filter(vinculo=Morador.LOCATARIO.value)
            unidades = condominio.unidades.all()
            # unidades = condominio.unidades\
            #     .annotate(proprietario_id=Subquery(proprietario_subquery.values('pessoa_id'))) \
            #     .annotate(locatario_id=Subquery(locatario_subquery.values('pessoa_id'))) \
            #     .all()
            despesas = condominio.despesas.filter(data__gte=data_inicio, data__lte=data_fim)
            for unidade in unidades:
                proprietario = PessoaUnidade.objects.filter(unidade=unidade, vinculo=Morador.PROPRIETARIO.value).first()
                locatario = PessoaUnidade.objects.filter(unidade=unidade, vinculo=Morador.LOCATARIO.value).first()
                fatura = Fatura()
                fatura.status = StatusFatura.ABERTO.value
                fatura.unidade = unidade
                fatura.data_vencimento = data_vencimento
                fatura.data_inicio = data_inicio
                fatura.data_fim = data_fim
                fatura.data_criacao = data_criacao
                fatura.competencia_mes = data_inicio.month
                fatura.competencia_ano = data_inicio.year
                # fatura.proprietario_id = unidade.proprietario_id
                # fatura.locatario_id = unidade.locatario_id
                fatura.proprietario_id = proprietario.pessoa_id
                if locatario:
                    fatura.locatario_id = locatario.pessoa_id
                fatura.valor = Decimal(0)
                fatura_despesas = []
                for despesa in despesas:
                    fatura_despesa = FaturaDespesa()
                    fatura_despesa.despesa = despesa
                    is_fracao = despesa.rateio == 'Fração'
                    if is_fracao:
                        fatura_despesa.valor = (despesa.valor * Decimal(unidade.fracao)).quantize(Decimal("0.00"))
                    else:
                        fatura_despesa.valor = despesa.valor / len(unidades)
                    fatura_despesas.append(fatura_despesa)
                    fatura.valor += fatura_despesa.valor
                fatura.save()
                for fatura_despesa in fatura_despesas:
                    fatura_despesa.fatura = fatura
                    fatura_despesa.save()
            return redirect('condominio:fatura_list', condominio_id=condominio_id)
    ctx = {'condominio': condominio}
    return render(request, 'condominio/fatura_form.html', ctx)


def fatura_pagamento(request, fatura_id):
    fatura = Fatura.objects.get(id=fatura_id)
    unidade = Unidade.objects.get(id=fatura.unidade.id)
    condominio = unidade.condominio

    context = {
        'fatura': fatura,
        'condominio': condominio,
    }

    if request.method == 'POST':
        form = FaturaPagarForm(request.POST)
        if not form.is_valid():
            context['erro_formulario'] = "Formulário inválido"
        else:
            data_pagamento = form.cleaned_data['data_pagamento']
            print("Data pagamento", data_pagamento)
            fatura.data_pagamento = data_pagamento
            fatura.status = StatusFatura.PAGO.value
            fatura.save()
            return redirect('condominio:fatura_list', unidade.condominio.id)
    return render(request, 'condominio/fatura_pagamento.html', context)


def fatura_pagamento_detalhe(request, fatura_id):
    fatura = Fatura.objects.get(id=fatura_id)
    unidade = Unidade.objects.get(id=fatura.unidade.id)
    condominio = unidade.condominio
    context = {
        'fatura': fatura,
        'condominio': condominio,
    }
    return render(request, 'condominio/fatura_pagamento_detalhe.html', context)


def faturas_em_atraso(condominio_id):
    condominio = Condominio.objects.get(id=condominio_id)
    ids_unidades = condominio.unidades.all().values('pk')
    faturas = Fatura.objects\
        .filter(unidade_id__in=ids_unidades)\
        .filter(data_vencimento__lt=timezone.now())\
        .filter(status = StatusFatura.ABERTO.value)
    faturas_em_atraso = len(faturas)
    return faturas_em_atraso


def faturas_em_aberto(condominio_id):
    condominio = Condominio.objects.get(id=condominio_id)
    ids_unidades = condominio.unidades.all().values('pk')
    faturas = Fatura.objects\
        .filter(unidade_id__in=ids_unidades)\
        .filter(status = 'ABERTO')
    faturas_todas = len(faturas)
    return faturas_todas


def fatura_vencida_calculo(request):

    data_pagamento = request.GET.get('data_pagamento')

    data = {
        'data_pagamento': data_pagamento,
    }
    return JsonResponse(data)


# Fatura Protótipo


def fatura_list2(request):
    return render(request, 'condominio/fatura_list2.html')  # noqa


def fatura_create2(request):
    return render(request, 'condominio/fatura_form2.html')  # noqa
