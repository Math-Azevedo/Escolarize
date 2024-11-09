# notas/views.py
from collections import defaultdict
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from usuarios.models import Aluno
from .models import Serie, Nota, Disciplina
from usuarios.models import Professor
from django.http import Http404

@login_required
def lista_series(request):
    if request.user.tipo_usuario == 'PROFESSOR':
        series = Serie.objects.filter(professores=request.user.professor)
    else:
        series = []
    return render(request, 'notas/lista_series.html', {'series': series})

@login_required
def alunos_serie(request, serie_id):
    serie = Serie.objects.get(id=serie_id)
    alunos = serie.aluno_set.all()
    notas = Nota.objects.filter(aluno__serie=serie)
    context = {
        'serie': serie,
        'alunos': alunos,
        'notas': notas
    }
    return render(request, 'notas/alunos_serie.html', context)

def series_view(request):
    # Verifica se o usuário logado é um professor
    professor = get_object_or_404(Professor, user=request.user)
    
    # Obtém as séries associadas ao professor
    series = professor.series.all()
    
    # Renderiza a página com a lista de séries
    return render(request, 'professor/series.html', {'series': series})

def series_professor_view(request):
    user = request.user
    if hasattr(user, 'professor'):
        professor = user.professor
        series = professor.series.all()
        return render(request, 'notas/lista_series.html', {'series': series})
    else:
        # Lida com o caso em que o usuário não é um professor
        return render(request, 'usuarios/login.html', {'series': []})


@login_required
def historico(request):
    # Tenta obter o objeto `Aluno` do usuário logado
    try:
        aluno_obj = request.user.aluno
    except Aluno.DoesNotExist:
        return render(request, 'notas/erro.html', {'mensagem': 'Aluno não encontrado para o usuário atual.'})

    # Filtra as notas pelo usuário relacionado ao `Aluno`
    notas = Nota.objects.filter(aluno=request.user).select_related('disciplina')
    historico_por_ano = defaultdict(lambda: defaultdict(list))
    medias_por_ano = defaultdict(dict)
    
    # Organiza notas por ano, disciplina e bimestre
    for nota in notas:
        historico_por_ano[nota.ano][nota.disciplina.nome].append({
            'nota': nota.valor,
            'bimestre': nota.bimestre
        })
    
    # Calcula a média para cada disciplina em cada ano
    for ano, disciplinas in historico_por_ano.items():
        for disciplina, notas_list in disciplinas.items():
            medias_por_ano[ano][disciplina] = sum(n['nota'] for n in notas_list) / len(notas_list)

    context = {
        'historico_por_ano': historico_por_ano,
        'medias_por_ano': medias_por_ano
    }
    return render(request, 'notas/historico.html', context)


@login_required
def lancar_notas(request, serie_id):
    serie = get_object_or_404(Serie, id=serie_id)
    alunos = Aluno.objects.filter(serie=serie)
    disciplinas = Disciplina.objects.all()
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                for aluno in alunos:
                    for disciplina in disciplinas:
                        nota1_field = f'nota1_{aluno.id}_{disciplina.id}'
                        nota2_field = f'nota2_{aluno.id}_{disciplina.id}'
                        nota3_field = f'nota3_{aluno.id}_{disciplina.id}'
                        nota4_field = f'nota4_{aluno.id}_{disciplina.id}'
                        
                        nota1 = float(request.POST.get(nota1_field, 0))
                        nota2 = float(request.POST.get(nota2_field, 0))
                        nota3 = float(request.POST.get(nota3_field, 0))
                        nota4 = float(request.POST.get(nota4_field, 0))
                        
                        if not (0 <= nota1 <= 10 and 0 <= nota2 <= 10 and 0 <= nota3 <= 10 and 0 <= nota4 <= 10):
                            raise ValueError(f'Notas devem estar entre 0 e 10 para o aluno {aluno.nome}')
                        
                        media = (nota1 + nota2 + nota3 + nota4) / 4
                        aprovado = media >= 7
                        
                        Nota.objects.update_or_create(
                            aluno=aluno,
                            disciplina=disciplina,
                            defaults={
                                'nota1': nota1,
                                'nota2': nota2,
                                'nota3': nota3,
                                'nota4': nota4,
                                'media': media,
                                'aprovado': aprovado
                            }
                        )
                
                messages.success(request, 'Notas lançadas com sucesso!')
                return redirect('lista_alunos', serie_id=serie_id)
                
        except ValueError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, 'Erro ao lançar notas. Verifique os dados e tente novamente.')
    
    context = {
        'serie': serie,
        'alunos': alunos,
        'disciplinas': disciplinas
    }
    return render(request, 'notas/lancar_notas.html', context)
