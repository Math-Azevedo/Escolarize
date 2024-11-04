# notas/views.py
from collections import defaultdict
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from usuarios.models import Aluno
from .models import  Serie, Nota, Disciplina

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

@login_required
def historico(request):
    notas = Nota.objects.filter(aluno=request.user).select_related('disciplina')
    historico_por_ano = defaultdict(lambda: defaultdict(list))
    medias_por_ano = defaultdict(dict)
    
    for nota in notas:
        historico_por_ano[nota.ano][nota.disciplina.nome].append({
            'nota': nota.valor,
            'bimestre': nota.bimestre
        })
    
    # Calcula média anual por disciplina
    for ano, disciplinas in historico_por_ano.items():
        for disciplina, notas in disciplinas.items():
            medias_por_ano[ano][disciplina] = sum(n['nota'] for n in notas) / len(notas)

    context = {
        'historico_por_ano': historico_por_ano,
        'medias_por_ano': medias_por_ano
    }
    return render(request, 'notas/historico.html', context)


@login_required
def lancar_notas(request, serie_id):
    # Busca a série ou retorna 404 se não existir
    serie = get_object_or_404(Serie, id=serie_id)
    
    # Busca todos os alunos da série
    alunos = Aluno.objects.filter(serie=serie)
    
    # Busca todas as disciplinas
    disciplinas = Disciplina.objects.all()
    
    if request.method == 'POST':
        try:
            with transaction.atomic():  # Usa transação para garantir integridade dos dados
                for aluno in alunos:
                    for disciplina in disciplinas:
                        # Constrói os nomes dos campos do formulário
                        nota1_field = f'nota1_{aluno.id}_{disciplina.id}'
                        nota2_field = f'nota2_{aluno.id}_{disciplina.id}'
                        nota3_field = f'nota3_{aluno.id}_{disciplina.id}'
                        nota4_field = f'nota4_{aluno.id}_{disciplina.id}'
                        
                        # Obtém as notas do formulário
                        nota1 = float(request.POST.get(nota1_field, 0))
                        nota2 = float(request.POST.get(nota2_field, 0))
                        nota3 = float(request.POST.get(nota3_field, 0))
                        nota4 = float(request.POST.get(nota4_field, 0))
                        
                        # Validação das notas
                        if not (0 <= nota1 <= 10 and 0 <= nota2 <= 10 and 
                               0 <= nota3 <= 10 and 0 <= nota4 <= 10):
                            raise ValueError(f'Notas devem estar entre 0 e 10 para o aluno {aluno.nome}')
                        
                        # Calcula a média
                        media = (nota1 + nota2 + nota3 + nota4) / 4
                        
                        # Determina se foi aprovado (média >= 7)
                        aprovado = media >= 7
                        
                        # Busca ou cria um registro de nota
                        nota, created = Nota.objects.update_or_create(
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
    
    # Prepara os dados para o template
    context = {
        'serie': serie,
        'alunos': alunos,
        'disciplinas': disciplinas,
        # Busca notas existentes para preencher o formulário
        'notas': {
            (nota.aluno_id, nota.disciplina_id): nota 
            for nota in Nota.objects.filter(aluno__serie=serie)
        }
    }
    
    return render(request, 'notas/lancar_notas.html', context)