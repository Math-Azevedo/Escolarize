# Generated by Django 5.1.2 on 2024-11-12 13:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('notas', '0001_initial'),
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='alunomateria',
            name='aluno',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='materias_cursadas', to='usuarios.aluno'),
        ),
        migrations.AddField(
            model_name='alunomateria',
            name='materia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='alunos_matriculados', to='notas.materia'),
        ),
        migrations.AddField(
            model_name='nota',
            name='aluno',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuarios.aluno'),
        ),
        migrations.AddField(
            model_name='nota',
            name='materia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='notas.materia'),
        ),
        migrations.AddField(
            model_name='notaserie',
            name='serie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='notas.serie'),
        ),
        migrations.AddField(
            model_name='materia',
            name='serie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='materias', to='notas.serie'),
        ),
        migrations.AddField(
            model_name='disciplina',
            name='serie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='disciplina', to='notas.serie'),
        ),
        migrations.AlterUniqueTogether(
            name='alunomateria',
            unique_together={('aluno', 'materia', 'ano_letivo', 'periodo')},
        ),
    ]
