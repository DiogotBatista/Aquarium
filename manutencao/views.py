# aquarios/views.py

import json

from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.dateparse import parse_date

from .forms import CustomUserCreationForm, AquarioForm, ManutencaoForm, PopulacaoForm, EspecimeForm, NotasForm
from .models import Aquario, Populacao, Especime, Manutencao, Aviso, Tipo_Especime, Notas

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')  # Adiciona mensagem de erro
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirecionar para a página de login ou onde preferir
            messages.success(request,
                             'Usuário cadastrado com sucesso! Por favor, faça o login com seu e-mail.')  # Mensagem de sucesso
            return redirect('login')
        else:
            # Formulário inválido, os erros serão passados para o template
            return render(request, 'register.html', {'form': form})
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('login')


def index(request):
    avisos = Aviso.objects.all()
    context = {
        'is_in_equipe': request.user.is_in_equipe_group() if request.user.is_authenticated else False,
        'avisos': avisos,
    }
    return render(request, 'index.html', context)


''' AQUARIO '''

@login_required
def aquario_list(request):
    if request.method == 'POST':
        form = AquarioForm(request.POST, request.FILES)
        if form.is_valid():
            novo_aquario = form.save(commit=False)
            novo_aquario.usuario = request.user
            novo_aquario.save()
            messages.success(request, 'Aquario cadastrado com sucesso!')  # Mensagem de sucesso
            return redirect('aquario_list')
    else:
        form = AquarioForm()
    aquarios = Aquario.objects.filter(usuario=request.user)
    return render(request, 'aquario_list.html', {'aquarios': aquarios, 'form': form})


@login_required
def aquario_create(request):
    if request.method == 'POST':
        form = AquarioForm(request.POST, request.FILES)
        if form.is_valid():
            aquario = form.save(commit=False)
            aquario.usuario = request.user
            aquario.save()
            messages.success(request, 'Aquário cadastrado com sucesso!')
            return redirect('aquario_list')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')  # Adiciona mensagem de erro
    else:
        form = AquarioForm()
    return render(request, 'add_aquario.html', {'form': form})


def aquario_detail(request, pk):
    aquario = get_object_or_404(Aquario, pk=pk, usuario=request.user)
    form = AquarioForm(instance=aquario)  # Instância do form preenchida com os dados do aquário
    return render(request, 'aquario_detail.html', {'aquario': aquario, 'form': form})


@login_required
def aquario_update(request, pk):
    aquario = get_object_or_404(Aquario, pk=pk)
    if request.method == 'POST':
        form = AquarioForm(request.POST, request.FILES, instance=aquario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Aquario atualizado com sucesso!')  # Mensagem de sucesso
            return redirect('aquario_detail', pk=aquario.pk)
    else:
        form = AquarioForm(instance=aquario)
    # Passa o form no contexto se for para usar na mesma página
    return render(request, 'aquario_detail.html', {'aquario': aquario, 'form': form})


@login_required
def aquario_delete(request, pk):
    aquario = get_object_or_404(Aquario, pk=pk, usuario=request.user)
    if request.method == 'POST':
        aquario.delete()
        messages.success(request, 'Aquário excluído com sucesso.')  # Opcional: adicionar mensagem de sucesso
        return redirect('aquario_list')
    else:
        # Se não for POST, você pode redirecionar para outra página ou mostrar uma mensagem de erro
        return redirect('aquario_detail', pk=pk)


''' MANUTENCAO '''


@login_required
def manutencao_create(request, aquario_pk):
    aquario = get_object_or_404(Aquario, pk=aquario_pk, usuario=request.user)
    if request.method == 'POST':
        print(request.POST)
        form = ManutencaoForm(request.POST)

        if form.is_valid():
            manutencao = form.save(commit=False)
            manutencao.aquario = aquario
            manutencao.save()
            messages.success(request, 'Manutenção adicionada com sucesso!')
            return redirect('manutencao_list', aquario_pk=aquario.pk)
    else:
        form = ManutencaoForm()
    # Para um modal, este retorno pode não ser necessário, mas é útil se não estiver usando AJAX.
    return render(request, 'manutencao_list.html', {'form': form, 'aquario': aquario})


@login_required
def manutencao_list(request, aquario_pk):
    aquario = get_object_or_404(Aquario, pk=aquario_pk, usuario=request.user)
    form = ManutencaoForm()

    # Recebe as datas do formulário
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')

    # Converte strings de data para objetos date, se presente
    data_inicio = parse_date(data_inicio) if data_inicio else None
    data_fim = parse_date(data_fim) if data_fim else None

    # Filtra manutenções baseado nas datas
    if data_inicio and data_fim:
        manutencoes_list = aquario.manutencoes.filter(data__range=[data_inicio, data_fim])
    else:
        manutencoes_list = aquario.manutencoes.all()

    # Paginação
    paginator = Paginator(manutencoes_list, 5)  # Mostra 5 manutenções por página
    page_number = request.GET.get('page')
    manutencoes = paginator.get_page(page_number)

    return render(request, 'manutencao_list.html', {'form': form, 'aquario': aquario, 'manutencoes': manutencoes})


@login_required
def manutencao_edit(request, aquario_pk, pk):
    manutencao = get_object_or_404(Manutencao, pk=pk, aquario__pk=aquario_pk)
    if request.method == 'POST':
        # print(request.POST)
        form = ManutencaoForm(request.POST, instance=manutencao)
        if form.is_valid():
            form.save()
            messages.success(request, 'Manutenção atualizada com sucesso!')
            return redirect('manutencao_list', aquario_pk=aquario_pk)
    else:
        form = ManutencaoForm(instance=manutencao)
        # print(manutencao.data)  # Verifique o formato da data antes de
    return render(request, 'manutencao_edit.html', {'form': form, 'aquario_pk': aquario_pk})


@login_required
def manutencao_delete(request, aquario_pk, pk):
    manutencao = get_object_or_404(Manutencao, pk=pk, aquario__pk=aquario_pk)
    if request.method == 'POST':
        manutencao.delete()
        messages.success(request, 'Manutenção excluída com sucesso.')
        return redirect('manutencao_list', aquario_pk=aquario_pk)
    return render(request, 'manutencao_confirm_delete.html', {'manutencao': manutencao, 'aquario_pk': aquario_pk})


''' NOTAS'''


@login_required
def notas_create(request, aquario_pk):
    aquario = get_object_or_404(Aquario, pk=aquario_pk, usuario=request.user)
    if request.method == 'POST':
        # print(request.POST)
        form = NotasForm(request.POST)

        if form.is_valid():
            notas = form.save(commit=False)
            notas.aquario = aquario
            notas.save()
            messages.success(request, 'Nota adicionada com sucesso!')
            return redirect('notas_list', aquario_pk=aquario.pk)
    else:
        form = NotasForm()
    # Para um modal, este retorno pode não ser necessário, mas é útil se não estiver usando AJAX.
    return render(request, 'notas_list.html', {'form': form, 'aquario': aquario})


@login_required
def notas_list(request, aquario_pk):
    aquario = get_object_or_404(Aquario, pk=aquario_pk, usuario=request.user)
    form = NotasForm()

    # Recebe as datas do formulário
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')

    # Converte strings de data para objetos date, se presente
    data_inicio = parse_date(data_inicio) if data_inicio else None
    data_fim = parse_date(data_fim) if data_fim else None

    # Filtra notas baseado nas datas
    if data_inicio and data_fim:
        notas_list = aquario.notas.filter(data__range=[data_inicio, data_fim])
    else:
        notas_list = aquario.notas.all()

    # Paginação
    paginator = Paginator(notas_list, 5)  # Mostra 5 notas por página
    page_number = request.GET.get('page')
    notas = paginator.get_page(page_number)

    return render(request, 'notas_list.html', {'form': form, 'aquario': aquario, 'notas': notas})


@login_required
def notas_edit(request, aquario_pk, pk):
    nota = get_object_or_404(Notas, pk=pk, aquario__pk=aquario_pk)
    if request.method == 'POST':
        # print(request.POST)
        form = NotasForm(request.POST, instance=nota)
        if form.is_valid():
            form.save()
            messages.success(request, 'Nota atualizada com sucesso!')
            return redirect('notas_list', aquario_pk=aquario_pk)
    else:
        form = NotasForm(instance=nota)
        # print(manutencao.data)  # Verifique o formato da data antes de
    return render(request, 'notas_edit.html', {'nota': nota, 'form': form, 'aquario_pk': aquario_pk})


@login_required
def notas_delete(request, aquario_pk, pk):
    nota = get_object_or_404(Notas, pk=pk, aquario__pk=aquario_pk)
    if request.method == 'POST':
        nota.delete()
        messages.success(request, 'Nota excluída com sucesso.')
        return redirect('notas_list', aquario_pk=aquario_pk)
    return render(request, 'notas_confirm_delete.html', {'notas': nota, 'aquario_pk': aquario_pk})


'''POPULACAO'''


@login_required
def populacao_list(request, pk):
    aquario = get_object_or_404(Aquario, pk=pk, usuario=request.user)
    queryset = Populacao.objects.filter(aquario=aquario)
    tipo_especime_list = Tipo_Especime.objects.all()

    # Captura o parâmetro de pesquisa da query string
    query = request.GET.get('q', '')
    if query:
        queryset = queryset.filter(especime__nome_popular__icontains=query)

    # Captura o parâmetro de tipo da query string
    tipo_especime_ids = request.GET.getlist('tipo_especime', '')
    if tipo_especime_ids:
        queryset = queryset.filter(especime__tipo_especime__id__in=tipo_especime_ids)

    soma_peixes = queryset.aggregate(soma=Sum('quantidade'))['soma'] or 0

    # Paginação
    paginator = Paginator(queryset, 5)  # Mostra 5 itens de população por página
    page_number = request.GET.get('page')
    populacao = paginator.get_page(page_number)

    context = {
        'aquario': aquario,
        'populacao': populacao,  # Utiliza o queryset filtrado
        'soma_peixes': soma_peixes,
        'tipo_especime_list': tipo_especime_list,
        'form': PopulacaoForm(),
        'query': query,  # Adiciona a pesquisa atual ao contexto
        'tipo_especime_ids': tipo_especime_ids,
        # Adiciona o tipo_especime_id ao contexto para controle dos botões de filtro
    }

    return render(request, 'populacao_list.html', context)


@login_required
def populacao_create(request, pk):
    aquario = get_object_or_404(Aquario, pk=pk)
    if request.method == 'POST':
        form = PopulacaoForm(request.POST)
        if form.is_valid():
            populacao = form.save(commit=False)
            populacao.aquario = aquario
            populacao.save()
            messages.success(request, 'Aquario cadastrado com sucesso!')  # Mensagem de sucesso
            # Redirecionar para a lista de população do aquário ou outra página conforme necessário
            return redirect('populacao_list', pk=aquario.pk)
    else:
        form = PopulacaoForm()
    return render(request, 'populacao_list.html', {'form': form, 'aquario': aquario})


@login_required
def populacao_edit(request, aquario_pk, pk):
    populacao = get_object_or_404(Populacao, pk=pk, aquario__pk=aquario_pk, aquario__usuario=request.user)
    if request.method == 'POST':
        form = PopulacaoForm(request.POST, instance=populacao)
        if form.is_valid():
            form.save()
            messages.success(request, 'População atualizada com sucesso!')
            return redirect('populacao_list', pk=aquario_pk)
    else:
        form = PopulacaoForm(instance=populacao)
    return render(request, 'populacao_edit.html', {'form': form, 'aquario': populacao.aquario})


@login_required
def populacao_delete(request, aquario_pk, pk):
    populacao = get_object_or_404(Populacao, pk=pk, aquario__pk=aquario_pk, aquario__usuario=request.user)
    if request.method == 'POST':
        populacao.delete()
        messages.success(request, 'População excluída com sucesso.')
        return redirect('populacao_list', pk=aquario_pk)
    return render(request, 'populacao_delete.html', {'populacao': populacao})


''' ESPECIME '''


def especie_detalhes_view(request, pk):
    especime = get_object_or_404(Especime, pk=pk)
    is_superuser = request.user.is_superuser
    usuario_no_grupo_equipe = request.user.groups.filter(name='equipe').exists()
    from_page = request.GET.get('from', '')
    context = {
        'is_superuser': is_superuser,
        'usuario_no_grupo_equipe': usuario_no_grupo_equipe,
        'especime': especime,
        'pk': pk,
        'from_page': from_page,

    }
    return render(request, 'especime_detail.html', context)


def cadastrar_especime(request):
    is_superuser = request.user.is_superuser
    usuario_no_grupo_equipe = request.user.groups.filter(name='equipe').exists()

    # Verifica se o usuário é superusuário ou pertence ao grupo 'topografia'
    if not (is_superuser or usuario_no_grupo_equipe):
        raise PermissionDenied

    if request.method == 'POST':
        form = EspecimeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Espécime cadastrada com sucesso!')
            return redirect('especime_list')  # Substitua 'especimes_lista' pela URL de destino após o cadastro
    else:
        form = EspecimeForm()
    return render(request, 'cadastrar_especime.html', {'form': form})


def especime_list(request):
    is_superuser = request.user.is_superuser
    usuario_no_grupo_equipe = request.user.groups.filter(name='equipe').exists()

    # Verifica se o usuário é superusuário ou pertence ao grupo 'Equipe'
    if not (is_superuser or usuario_no_grupo_equipe):
        raise PermissionDenied

    # Captura o parâmetro de pesquisa da query string
    query = request.GET.get('q', '')
    queryset = Especime.objects.all()
    if query:
        queryset = queryset.filter(nome_popular__icontains=query)

    # Captura o parâmetro de tipo da query string
    tipo_especime_ids = request.GET.getlist('tipo_especime')
    if tipo_especime_ids:
        queryset = queryset.filter(tipo_especime__id__in=tipo_especime_ids)

    # Adicionando paginação
    paginator = Paginator(queryset, 6)  # Altere 10 para quantos itens você quer por página
    page_number = request.GET.get('page')
    especimes_page = paginator.get_page(page_number)

    context = {
        'especimes': especimes_page,
        'tipo_especime_list': Tipo_Especime.objects.all(),
        'query': query,  # Adiciona a pesquisa atual ao contexto
        'tipo_especime_ids': tipo_especime_ids,
        # Adiciona o tipo_especime_id ao contexto para controle dos botões de filtro
    }

    return render(request, 'especime_list.html', context)


@login_required
def especime_edit(request, pk):
    is_superuser = request.user.is_superuser
    usuario_no_grupo_equipe = request.user.groups.filter(name='equipe').exists()

    # Verifica se o usuário é superusuário ou pertence ao grupo 'topografia'
    if not (is_superuser or usuario_no_grupo_equipe):
        raise PermissionDenied

    especime = get_object_or_404(Especime, pk=pk)
    if request.method == 'POST':
        form = EspecimeForm(request.POST, request.FILES, instance=especime)
        if form.is_valid():
            form.save()
            messages.success(request, 'Espécime atualizado com sucesso!')
            return redirect('especime_detail', pk=pk)  # Redirecione para a página de detalhes do espécime
    else:
        form = EspecimeForm(instance=especime)
    return render(request, 'cadastrar_especime.html',
                  {'form': form, 'especime_pk': pk, 'nome_especie': especime.nome_popular, })


''' GRAFICOS '''


@login_required
def visualizar_graficos(request, aquario_pk):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    aquario = get_object_or_404(Aquario, pk=aquario_pk)

    # Filtro inicial para manutenções deste aquário, agora com ordenação por data
    manutencoes_query = aquario.manutencoes.all().order_by('data')

    # Aplicação dos filtros de datas
    if start_date:
        manutencoes_query = manutencoes_query.filter(data__gte=start_date)
    if end_date:
        manutencoes_query = manutencoes_query.filter(data__lte=end_date)

    # Extração dos dados após aplicação dos filtros
    datas = [manutencao.data.strftime("%d/%m/%Y") for manutencao in manutencoes_query]
    phs = [float(manutencao.ph) for manutencao in manutencoes_query if manutencao.ph]
    temperaturas = [float(manutencao.temperatura) for manutencao in manutencoes_query if manutencao.temperatura]

    context = {
        'aquario_pk': aquario_pk,
        'datas': json.dumps(datas),
        'phs': json.dumps(phs),
        'temperaturas': json.dumps(temperaturas),
    }

    return render(request, 'graficos.html', context)
