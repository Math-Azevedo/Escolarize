# mensagens/forms.py
from django import forms
from notas.models import Nota # Corrigindo os imports - removendo 'escolarize' do caminho
from usuarios.models import Usuario # Corrigindo os imports - removendo 'escolarize' do caminho
from .models import Mensagem

class MensagemForm(forms.ModelForm):
    class Meta:
        model = Mensagem
        fields = ['destinatario', 'assunto', 'conteudo']
        widgets = {
            'conteudo': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        if user and user.tipo_usuario == 'PROFESSOR':
            self.fields['destinatario'].queryset = Usuario.objects.filter(
                tipo_usuario='RESPONSAVEL'
            )
        elif user and user.tipo_usuario == 'RESPONSAVEL':
            self.fields['destinatario'].queryset = Usuario.objects.filter(
                tipo_usuario='PROFESSOR'
            )

class NotaBimestreFormSet(forms.BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queryset = Nota.objects.none()

class NotasBimestreForm(forms.Form):
    def __init__(self, *args, alunos, materias, bimestre, **kwargs):
        super().__init__(*args, **kwargs)
        
        for aluno in alunos:
            for materia in materias:
                field_name = f'nota_{aluno.id}_{materia.id}'
                self.fields[field_name] = forms.DecimalField(
                    max_digits=4,
                    decimal_places=2,
                    required=False,
                    widget=forms.NumberInput(attrs={
                        'class': 'form-control',
                        'step': '0.1',
                        'min': '0',
                        'max': '10'
                    })
                )
                
                # Tenta buscar nota existente
                try:
                    nota = Nota.objects.get(
                        aluno=aluno,
                        materia=materia,
                        bimestre=bimestre
                    )
                    self.initial[field_name] = nota.nota
                except Nota.DoesNotExist:
                    pass