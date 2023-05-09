from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

from condominio import views

app_name = 'condominio'

urlpatterns = [

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
    path('pessoa_detail/<int:pk>/', views.PessoaDetail.as_view(), name='pessoa_detail'),  # noqa

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

    # FATURA
    path('fatura_list/<int:condominio_id>/', views.fatura_list, name='fatura_list'),  # noqa
    path('fatura_create/<int:condominio_id>/', views.fatura_create, name='fatura_create'),  # noqa

    # FATURA PROTÓTIPO
    path('fatura_list2/', views.fatura_list2, name='fatura_list2'),  # noqa
    path('fatura_create2/', views.fatura_create2, name='fatura_create2'),  # noqa


    # FAVICON
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('img/favicon.ico')))  # noqa
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
