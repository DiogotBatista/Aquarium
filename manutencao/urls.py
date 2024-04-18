
from django.urls import path
from manutencao import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('aquario_list/', views.aquario_list, name= 'aquario_list'),
    path('aquarios/<int:pk>/', views.aquario_detail, name='aquario_detail'),
    path('aquario/new/', views.aquario_create, name='aquario_create'),
    path('aquario/edit/<int:pk>/', views.aquario_update, name='aquario_update'),
    path('aquario/delete/<int:pk>/', views.aquario_delete, name='aquario_delete'),
    path('aquarios/<int:pk>/populacao/', views.populacao_list, name='populacao_list'),
    path('aquario/<int:pk>/populacao/adicionar/', views.populacao_create, name='populacao_create'),
    path('aquario/<int:aquario_pk>/populacao/editar/<int:pk>/', views.populacao_edit, name='populacao_edit'),
    path('aquario/<int:aquario_pk>/populacao/excluir/<int:pk>/', views.populacao_delete, name='populacao_delete'),
    path('especimes/cadastrar/', views.cadastrar_especime, name='cadastrar_especime'),
    path('especie/detalhes/<int:pk>/', views.especie_detalhes_view, name='especime_detail'),
    path('especimes_list/', views.especime_list, name='especime_list'),
    path('especimes/editar/<int:pk>/', views.especime_edit, name='especime_edit'),
    path('aquario/<int:aquario_pk>/manutencao/new/', views.manutencao_create, name='manutencao_create'),
    path('aquario/<int:aquario_pk>/manutencoes/', views.manutencao_list, name='manutencao_list'),
    path('aquario/<int:aquario_pk>/manutencao/editar/<int:pk>/', views.manutencao_edit, name='manutencao_edit'),
    path('aquario/<int:aquario_pk>/manutencao/excluir/<int:pk>/', views.manutencao_delete, name='manutencao_delete'),
    path('aquarios/<int:aquario_pk>/graficos/', views.visualizar_graficos, name='visualizar_graficos'),

    path('aquario/<int:aquario_pk>/notas/new/', views.notas_create, name='notas_create'),
    path('aquario/<int:aquario_pk>/notas/', views.notas_list, name='notas_list'),
    path('aquario/<int:aquario_pk>/notas/editar/<int:pk>/', views.notas_edit,name='notas_edit'),
    path('aquario/<int:aquario_pk>/notas/excluir/<int:pk>/', views.notas_delete,name='notas_delete'),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)