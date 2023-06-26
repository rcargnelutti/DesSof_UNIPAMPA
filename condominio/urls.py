from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

from condominio import views

app_name = 'condominio'

urlpatterns = [

    # FAVICON
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('img/favicon.ico'))),  # noqa

    # CONDOMINIO
    path('', views.CondominioList.as_view(), name='list'),
    path('create/', views.CondominioCreate.as_view(), name='create'),
    path('update/<int:pk>/', views.CondominioUpdate.as_view(), name='update'),
    path('detail/<int:pk>/', views.CondominioDetail.as_view(), name='detail'),
    path('delete/<int:pk>/', views.CondominioDelete.as_view(), name='delete'),
    path('gestao/<int:condominio_id>/', views.condominio_gestao, name='gestao'),  # noqa

    # UNIDADE
    path('unidade_list/<int:condominio_id>/', views.unidade_list, name='unidade_list'),  # noqa
    path('unidade_create/<int:condominio_id>/', views.unidade_create, name='unidade_create'),  # noqa
    path('unidade_update/<int:unidade_id>/', views.unidade_update, name='unidade_update'),  # noqa
    path('unidade_confirm_delete/<int:unidade_id>/', views.unidade_confirm_delete, name='unidade_confirm_delete'),  # noqa
    path('unidade_delete/<int:unidade_id>/', views.unidade_delete, name='unidade_delete'),  # noqa

    # PESSOA
    path('pessoa_list/', views.PessoaList.as_view(), name='pessoa_list'),  # noqa
    path('pessoa_create/', views.PessoaCreate.as_view(), name='pessoa_create'),
    path('pessoa_update/<int:pk>/', views.PessoaUpdate.as_view(), name='pessoa_update'),  # noqa
    #path('pessoa_detail/<int:pk>/', views.PessoaDetail.as_view(), name='pessoa_detail'),  # noqa
    path('pessoa_detail/<int:pessoa_id>/', views.pessoa_detail, name='pessoa_detail'),  # noqa

    # PESSOA UNIDADE - VINCULO / MORADOR
    path('pessoa_unidade_list/<int:unidade_id>/', views.pessoa_unidade_list, name='pessoa_unidade_list'),  # noqa
    path('pessoa_unidade_create/<int:unidade_id>/', views.pessoa_unidade_create, name='pessoa_unidade_create'),  # noqa
    path('pessoa_unidade_update/<int:pessoa_unidade_id>/', views.pessoa_unidade_update, name='pessoa_unidade_update'),  # noqa

    # CONTA
    path('conta_list/<int:condominio_id>/', views.conta_list, name='conta_list'),  # noqa
    path('conta_create/<int:condominio_id>/', views.conta_create, name='conta_create'),  # noqa
    path('conta_update/<int:conta_id>/', views.conta_update, name='conta_update'),  # noqa

    # DESPESAS
    path('despesa_list/<int:condominio_id>/', views.despesa_list, name='despesa_list'),  # noqa
    path('despesa_create/<int:condominio_id>/', views.despesa_create, name='despesa_create'),  # noqa
    path('despesa_update/<int:despesa_id>/', views.despesa_update, name='despesa_update'),  # noqa
    path('despesa_confirm_delete/<int:despesa_id>/', views.despesa_confirm_delete, name='despesa_confirm_delete'),  # noqa
    path('despesa_delete/<int:despesa_id>/', views.despesa_delete, name='despesa_delete'),  # noqa

    path('despesa_unidade_list/<int:unidade_id>/', views.despesa_unidade_list, name='despesa_unidade_list'),  # noqa
    path('despesa_unidade_create/<int:unidade_id>/', views.despesa_unidade_create, name='despesa_unidade_create'),  # noqa
    path('despesa_unidade_update/<int:despesa_id>/', views.despesa_unidade_update, name='despesa_unidade_update'),  # noqa

    # FATURA
    path('fatura_list/<int:condominio_id>/', views.fatura_list, name='fatura_list'),  # noqa
    path('fatura_create/<int:condominio_id>/', views.fatura_create, name='fatura_create'),  # noqa
    path('fatura_pagamento/<int:fatura_id>/', views.fatura_pagamento, name='fatura_pagamento'),  # noqa
    path('fatura_pagamento_detalhe/<int:fatura_id>/', views.fatura_pagamento_detalhe, name='fatura_pagamento_detalhe'),  # noqa
    path('ajax/fatura_vencida_calculo/', views.fatura_vencida_calculo, name='fatura_vencida_calculo'),  # noqa

    # RELATÓRIOS
    path('relatorio_list/<int:condominio_id>/', views.relatorio_list, name='relatorio_list'),  # noqa
    path('relatorio_despesa/<int:condominio_id>/', views.relatorio_despesa, name='relatorio_despesa'),  # noqa
    path('relatorio_pessoa_unidade/<int:condominio_id>/', views.relatorio_pessoa_unidade, name='relatorio_pessoa_unidade'),  # noqa
    path('relatorio_pessoa_contato/<int:condominio_id>/', views.relatorio_pessoa_contato, name='relatorio_pessoa_contato'),  # noqa

    # CONTATOS
    path('contato_list/<int:pessoa_id>/', views.contato_list, name='contato_list'),  # noqa

    # CONTATOS - TELEFONE
    path('contato_telefone_create/<int:pessoa_id>/', views.contato_telefone_create, name='contato_telefone_create'),  # noqa
    path('contato_telefone_update/<int:telefone_id>/', views.contato_telefone_update, name='contato_telefone_update'),  # noqa
    path('contato_telefone_confirm_delete/<int:telefone_id>/', views.contato_telefone_confirm_delete, name='contato_telefone_confirm_delete'),  # noqa
    path('contato_telefone_delete/<int:telefone_id>/', views.contato_telefone_delete, name='contato_telefone_delete'),  # noqa

    # CONTATOS - EMAIL
    path('contato_email_create/<int:pessoa_id>/', views.contato_email_create, name='contato_email_create'),  # noqa
    path('contato_email_update/<int:email_id>/', views.contato_email_update, name='contato_email_update'),  # noqa
    path('contato_email_confirm_delete/<int:email_id>/', views.contato_email_confirm_delete, name='contato_email_confirm_delete'),  # noqa
    path('contato_email_delete/<int:email_id>/', views.contato_email_delete, name='contato_email_delete'),  # noqa
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
