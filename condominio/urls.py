from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

from condominio import views

app_name = 'condominio'

urlpatterns = [
    path('', views.CondominioList.as_view(), name='list'),
    path('create/', views.CondominioCreate.as_view(), name='create'),
    path('update/<int:pk>/', views.CondominioUpdate.as_view(), name='update'),
    path('detail/<int:pk>/', views.CondominioDetail.as_view(), name='detail'),
    path('delete/<int:pk>/', views.CondominioDelete.as_view(), name='delete'),
    path('gestao/<int:condominio_id>/', views.condominio_gestao, name='gestao'),


    path('unidade_list', views.UnidadeList.as_view(), name='unidade_list'),
    path('unidade_create', views.unidade_create, name='unidade_create'),

    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('img/favicon.ico')))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
