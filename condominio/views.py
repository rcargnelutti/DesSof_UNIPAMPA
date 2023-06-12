# from django.db.models import OuterRef, Subquery
from django.db.models import OuterRef, Subquery
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView  # noqa
from condominio.models import Condominio, Unidade, Pessoa, PessoaUnidade, Conta, Despesa, Fatura, Morador, FaturaDespesa, StatusFatura  # noqa
from condominio.forms import UnidadeForm, PessoaUnidadeForm, ContaForm, DespesaForm, FaturaForm, FaturaPagarForm, RelatorioForm  # noqa
from decimal import Decimal
from django.http import JsonResponse
from django.utils.dateparse import parse_date

# CONDOMÍNIO


class CondominioList(ListView):
    model = Condominio
    queryset = Condominio.objects.all()


class CondominioCreate(CreateView):
    model = Condominio
    fields = ['nome', 'documento', 'cep', 'endereco', 'numero', 'bairro', 'cidade', 'estado', 'pais',  # noqa
              'area_comum', 'area_privativa', 'area_total', 'dia_vencimento_boleto', 'multa', 'juro',]  # noqa
    success_url = reverse_lazy('condominio:list')


class CondominioUpdate(UpdateView):
    model = Condominio
    fields = fields = ['nome', 'documento', 'cep', 'endereco', 'numero', 'bairro', 'cidade', 'estado', 'pais',  # noqa
                       'area_comum', 'area_privativa', 'area_total', 'dia_vencimento_boleto', 'multa', 'juro',]  # noqa
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
    condominio = Condominio.objects.get(id=unidade.condominio.id)  # noqa
    return render(request, 'condominio/pessoa_unidade_list.html', {'unidade': unidade, 'pessoa_unidade': pessoa_unidade, 'condominio': condominio})  # noqa


def pessoa_unidade_create(request, unidade_id):
    unidade = Unidade.objects.get(id=unidade_id)
    condominio = Condominio.objects.get(id=unidade.condominio.id)  # noqa
    if request.method == "GET":
        form = PessoaUnidadeForm(initial={'unidade': unidade})
        return render(request, 'condominio/pessoa_unidade_form.html', {'unidade': unidade, 'condominio': condominio, 'form': form})  # noqa
    else:
        form = PessoaUnidadeForm(request.POST)
        if not form.is_valid():
            return render(request, 'condominio/pessoa_unidade_form.html', {'unidade': unidade, 'condominio': condominio, 'form': form})  # noqa
        pessoa_unidade = form.save(commit=False)
        pessoa_unidade.unidade = unidade
        pessoa_unidade.save()
        return redirect(f'/condominios/pessoa_unidade_list/{unidade_id}/')  # noqa


def pessoa_unidade_update(request, pessoa_unidade_id):
    pessoa_unidade = PessoaUnidade.objects.get(id=pessoa_unidade_id)
    unidade = Unidade.objects.get(id=pessoa_unidade.unidade.id)  # noqa
    condominio = Condominio.objects.get(id=unidade.condominio.id)  # noqa
    if request.method == "GET":
        form = PessoaUnidadeForm(instance=pessoa_unidade)
        return render(request, 'condominio/pessoa_unidade_form.html', {'unidade': unidade, 'condominio': condominio, 'form': form})  # noqa
    else:
        form = PessoaUnidadeForm(request.POST, instance=pessoa_unidade)
        if not form.is_valid():
            return render(request, 'condominio/pessoa_unidade_form.html', {'unidade': unidade, 'condominio': condominio, 'form': form})  # noqa
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
        form = DespesaForm(initial={'condominio': condominio}, condominio_id=condominio_id)  # noqa
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
        form = DespesaForm(request.POST, instance=despesa, condominio_id=condominio)  # noqa
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
        fatura.despesas_list = fatura.despesas.select_related('despesa__conta').all()  # noqa
    total_faturas = len(faturas)
    context = {'condominio': condominio, 'faturas': faturas, 'total_faturas': total_faturas}  # noqa
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
            # pessoa_subquery = PessoaUnidade.objects.filter(unidade_id=OuterRef('pk')) # noqa
            # proprietario_subquery = pessoa_subquery.filter(vinculo=Morador.PROPRIETARIO.value) # noqa
            # locatario_subquery = pessoa_subquery.filter(vinculo=Morador.LOCATARIO.value) # noqa
            unidades = condominio.unidades.all()
            # unidades = condominio.unidades\
            #     .annotate(proprietario_id=Subquery(proprietario_subquery.values('pessoa_id'))) \ # noqa
            #     .annotate(locatario_id=Subquery(locatario_subquery.values('pessoa_id'))) \ # noqa
            #     .all()
            despesas = condominio.despesas.filter(data__gte=data_inicio, data__lte=data_fim)  # noqa
            for unidade in unidades:
                proprietario = PessoaUnidade.objects.filter(unidade=unidade, vinculo=Morador.PROPRIETARIO.value).first()  # noqa
                locatario = PessoaUnidade.objects.filter(unidade=unidade, vinculo=Morador.LOCATARIO.value).first()  # noqa
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
                        fatura_despesa.valor = (despesa.valor * Decimal(unidade.fracao)).quantize(Decimal("0.00"))  # noqa
                    else:
                        fatura_despesa.valor = despesa.valor / len(unidades)
                    fatura_despesas.append(fatura_despesa)
                    fatura.valor += fatura_despesa.valor
                fatura.save()
                for fatura_despesa in fatura_despesas:
                    fatura_despesa.fatura = fatura
                    fatura_despesa.save()
            return redirect('condominio:fatura_list', condominio_id=condominio_id)  # noqa
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
            fatura.data_pagamento = data_pagamento

            valor_multa = form.cleaned_data['valor_multa']
            valor_juro = form.cleaned_data['valor_juro']
            valor_pago = form.cleaned_data['valor_pago']
            dias_atraso_pagamento = fatura_dias_atraso(data_pagamento, fatura.data_vencimento)  # noqa

            if valor_multa and valor_juro and valor_pago:
                fatura.valor_multa = valor_multa
                fatura.valor_juro = valor_juro
                fatura.valor_pago = valor_pago
                fatura.dias_atraso_pagamento = dias_atraso_pagamento
                print(fatura.dias_atraso_pagamento)
            fatura.status = StatusFatura.PAGO.value
            fatura.save()
            return redirect('condominio:fatura_list', unidade.condominio.id)
    return render(request, 'condominio/fatura_pagamento.html', context)


def fatura_pagamento_detalhe(request, fatura_id):
    fatura = Fatura.objects.get(id=fatura_id)
    unidade = Unidade.objects.get(id=fatura.unidade.id)
    condominio = unidade.condominio
    condominio.juro_dia = condominio.juro/30
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
        .filter(status=StatusFatura.ABERTO.value)
    faturas_em_atraso = len(faturas)
    return faturas_em_atraso


def faturas_em_aberto(condominio_id):
    condominio = Condominio.objects.get(id=condominio_id)
    ids_unidades = condominio.unidades.all().values('pk')
    faturas = Fatura.objects\
        .filter(unidade_id__in=ids_unidades)\
        .filter(status='ABERTO')
    faturas_todas = len(faturas)
    return faturas_todas


def fatura_dias_atraso(data1, data2):
    dias_atraso = abs((data1 - data2).days)
    return dias_atraso


def fatura_vencida_calculo(request):
    data_pagamento = parse_date(request.GET.get('data_pagamento'))
    fatura_id = int(request.GET.get('fatura_id'))
    fatura = Fatura.objects.get(id=fatura_id)
    unidade = Unidade.objects.get(id=fatura.unidade.id)
    condominio = Condominio.objects.get(id=unidade.condominio.id)

    dias_atraso = 0
    valor_multa = 0
    valor_juro = 0
    valor_pago = 0
    if data_pagamento > fatura.data_vencimento:
        # dias_atraso = abs((data_pagamento - fatura.data_vencimento).days)
        dias_atraso = fatura_dias_atraso(data_pagamento, fatura.data_vencimento)  # noqa
        valor_juro = ((((condominio.juro/30) * dias_atraso) * fatura.valor) / 100).quantize(Decimal("0.00"))  # noqa
        valor_multa = ((condominio.multa * fatura.valor) / 100).quantize(Decimal("0.00"))  # noqa
        valor_pago = (fatura.valor + valor_juro + valor_multa).quantize(Decimal("0.00"))  # noqa

    data = {
        'dias_atraso': dias_atraso,
        'valor_multa': valor_multa,
        'valor_juro': valor_juro,
        'valor_pago': valor_pago,
    }
    return JsonResponse(data)


# Relatórios


def relatorio_list(request, condominio_id):
    condominio = Condominio.objects.get(id=condominio_id)
    context = {'condominio': condominio}
    return render(request, 'condominio/relatorio_list.html', context)  # noqa


def relatorio_despesa(request, condominio_id):
    ctx = {}
    condominio = get_object_or_404(Condominio, pk=condominio_id)
    if request.method == 'POST':
        form = RelatorioForm(request.POST)
        if not form.is_valid():
            ctx['erro_formulario'] = "Formulário inválido"
        else:
            data_geracao = timezone.now()
            data_inicio = form.cleaned_data['data_inicio']
            data_fim = form.cleaned_data['data_fim']

            # despesas = condominio.despesas.order_by("-data").filter(data__gte=data_inicio, data__lte=data_fim).aggregate(Sum('valor'))
            # print ('{}'.format(despesas['valor__sum']))
            # total_periodo = ('{}'.format(despesas['valor__sum']))

            # despesas = condominio.despesas.order_by("-data").filter(data__gte=data_inicio, data__lte=data_fim).annotate(total_periodo=Sum('valor'))  # noqa

            despesas = condominio.despesas.order_by("-data").filter(data__gte=data_inicio, data__lte=data_fim)  # noqa
            total_periodo = 0
            for despesa in despesas:
                total_periodo += despesa.valor

            ctx = {
                'condominio': condominio,
                'despesas': despesas,
                'data_geracao': data_geracao,
                'data_inicio': data_inicio,
                'data_fim': data_fim,
                'total_periodo': total_periodo,
            }
            return render(request, 'condominio/relatorio_despesa_list.html', ctx)
    return render(request, 'condominio/relatorio_despesa_form.html', {'condominio': condominio})


def relatorio_pessoa_unidadeFatura(request, condominio_id):
    condominio = get_object_or_404(Condominio, pk=condominio_id)
    ids_unidades = condominio.unidades.all().values('pk')
    faturas = Fatura.objects\
        .select_related('unidade', 'proprietario', 'locatario')\
        .filter(unidade_id__in=ids_unidades)
    context = {'condominio': condominio, 'faturas': faturas}  # noqa
    return render(request, 'condominio/relatorio_pessoa_unidade.html', context)


def relatorio_pessoa_unidade2(request, condominio_id):
    condominio = get_object_or_404(Condominio, pk=condominio_id)
    ids_unidades = condominio.unidades.all().values('pk')
    pessoa_unidade = PessoaUnidade.objects\
        .filter(unidade_id__in=ids_unidades)\
        .filter(data_fim=None)
    context = {'condominio': condominio, 'pessoa_unidade': pessoa_unidade}  # noqa
    return render(request, 'condominio/relatorio_pessoa_unidade.html', context)


def relatorio_pessoa_unidade(request, condominio_id):
    condominio = get_object_or_404(Condominio, pk=condominio_id)
    pesssoas_query = PessoaUnidade.objects\
        .select_related('pessoa')\
        .filter(unidade_id=OuterRef('pk'), data_fim__isnull=True)
    proprietario_query = pesssoas_query.filter(vinculo=Morador.PROPRIETARIO.value)  # noqa
    locatario_query = pesssoas_query.filter(vinculo=Morador.LOCATARIO.value)
    unidades = condominio.unidades\
        .annotate(nome_proprietario=Subquery(proprietario_query.values('pessoa__nome'))) \
        .annotate(nome_locatario=Subquery(locatario_query.values('pessoa__nome'))) \
        .annotate(data_inicio_proprietario=Subquery(proprietario_query.values('data_inicio'))) \
        .annotate(data_inicio_locatario=Subquery(locatario_query.values('data_inicio'))) \
        .annotate(documento_proprietario=Subquery(proprietario_query.values('pessoa__documento'))) \
        .annotate(documento_locatario=Subquery(locatario_query.values('pessoa__documento'))) \
        .all()
    context = {'condominio': condominio, 'unidades': unidades}
    return render(request, 'condominio/relatorio_pessoa_unidade.html', context)
